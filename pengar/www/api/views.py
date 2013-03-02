import os

from datetime import datetime, timedelta

from sqlalchemy import func

from flask import abort, jsonify

from pengar.models import Account, Transaction
from pengar.database import db
from pengar.www import app

@app.route('/api/account/<int:account_id>')
def api_overview(account_id=None):
    days = int(os.environ.get('DAYS', 30))
    date_start = datetime.now() - timedelta(days=days)

    account = Account.query.filter_by(id=account_id).first()

    if account is None:
        abort(404)

    query = db.session.query(
            Transaction.date.label('date'),
            Transaction.note.label('note'),
            func.sum(Transaction.amount).label('amount')\
        ).filter(Transaction.date > date_start)\
        .filter(Transaction.amount < 0)\
        .filter(Transaction.account_id == account.id)\
        .group_by(Transaction.date, Transaction.note)\
        .order_by(Transaction.date.asc())

    serializable = []
    for t in query.all():
        s = t.__dict__
        s['date'] = s['date'].isoformat()
        s['amount'] = int(s['amount'] / -1)
        serializable.append(s)

    data = {}

    for s in serializable:
        data.setdefault(s['note'], [])
        data[s['note']].append(
            (s['date'], s['amount']))

    series = []

    for note, values in data.items():
        s = sorted(values, key=lambda x: x[0])

        last_date = -1
        dates = []

        for date, amount in s:
            # Set 'date' to days since first day in query
            date = (datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                    - date_start).days

            if not date == last_date + 1:
                # If there's a hole in the data before the current date, fill
                # it in
                for filler_date in range(last_date + 1, date):
                    dates.append([filler_date, 0])

            dates.append([date, amount])

            last_date = date

        if len(dates) < days + 1:
            # If there's a hole at the end of the dates, fill it in
            for filler_date in range(last_date + 1, days + 1):
                dates.append([filler_date, 0])

        for date in dates:
            series.append({
                'note': note,
                'date': (date_start + timedelta(date[0])).isoformat().split('.')[0],
                'amount': date[1]
            })

    return jsonify(series=series)


