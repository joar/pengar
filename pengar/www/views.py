import os
from pprint import PrettyPrinter
from datetime import datetime, timedelta

from sqlalchemy import func

from jinja2 import Markup

from flask import render_template, json, abort, flash, redirect, url_for, \
    session, g

from pengar.models import Transaction, Account
from pengar.database import db
from pengar.www import app
from pengar.www.util import login_user, update_accounts
from pengar.www.decorators import login_required
from pengar.www.models import User
from pengar.www.forms import RegistrationForm, LoginForm, UpdateForm

pp = PrettyPrinter(indent=4)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title=u'Pengar')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            form.errors.append(Markup(
                u'A user with email {0} already exists.'))
        else:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash(Markup(u'Welcome, <strong>{0}</strong>'.format(user.email)))
            return redirect(url_for('index'))

    return render_template(
        'account/register.html',
        form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.check_password(form.password.data):
                login_user(user)
                flash(Markup(u'Welcome back <strong>{0}</strong>'.format(
                    user.email)))
                return redirect(url_for('index'))
        else:
            form.errors.append(u'Invalid credentials')

    return render_template('account/login.html', form=form)


@app.route('/account/<int:account_id>')
@login_required
def overview(account_id=None):
    account = Account.query.filter_by(id=account_id).first()

    if account is None:
        abort(404)

    return render_template(
        'account.html',
        title=Markup(u'{0} &mdash; Overview &mdash; Pengar'.format(
            account.label)),
        account=account)


@app.route('/update', methods=['POST', 'GET'])
@login_required
def update():
    form = UpdateForm()

    if form.validate_on_submit():
        update_accounts(g.user.id, form.ssn.data, form.code.data)

    return render_template(
        'update.html',
        title=u'Update',
        form=form
    )

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect(url_for('see_you'))

@app.route('/see-you')
def see_you():
    return render_template('see-you.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html',
                           title=Markup(u'Privacy &mdash; Pengar'))
