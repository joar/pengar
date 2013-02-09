from flask import Flask, render_template, json
from flask.ext.bootstrap import Bootstrap

from jinja2 import Markup

from pengar.models import Transaction

from pprint import PrettyPrinter
import config
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(config)

bootstrap = Bootstrap(app)

pp = PrettyPrinter(indent=4)

@app.route('/')
def index():
    days = 30
    date_start = datetime.now() - timedelta(days=days)

    transactions = Transaction.query\
            .filter(Transaction.date > date_start)\
            .filter(Transaction.amount < 0)\
            .order_by(Transaction.date.asc()).all()

    serializable = []
    for t in transactions:
        s = t.serializable
        s['amount'] /= -1
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

        app.logger.debug(u'dates for {2} ({1}): {0}'.format(
            pp.pformat(dates),
            len(dates),
            note
        ))

        for date in dates:
            series.append({
                'note': note,
                'date': (date_start + timedelta(date[0])).isoformat().split('.')[0],
                'amount': date[1]
            })

    app.logger.debug('series: {0}'.format(pp.pformat(series)))


    return render_template(
        'index.html',
        title=Markup(u'Overview &mdash; Pengar'),
        series=json.dumps(series)
    )


@app.route('/update')
def update():
    return render_template(
        'update.html',
        title=u'Update'
    )
