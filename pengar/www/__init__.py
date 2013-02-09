from flask import Flask, render_template, json
from flask.ext.bootstrap import Bootstrap

from pengar.models import Transaction

import config
import re

app = Flask(__name__)
app.config.from_object(config)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.asc()).all()

    series_data = {}

    for transaction in transactions:
        series_data.setdefault(transaction.note, [])
        serializable = transaction.serializable

        series_data[transaction.note].append(serializable)

    # Create a list of series
    series = map(
        lambda value: {
            # Get the note from the first dict() item in the list
            'name': value[0]['note'],
            # Create the datapoints
            'data': map(
                lambda x:
                    [
                        x['date'],
                        x['amount']
                    ], value)
        },
        series_data.values())

    series_json = json.dumps(series)

    series_json = re.sub(
        r'("(?P<year>\d{4})-0?(?P<month>\d{1,2})-0?(?P<day>\d{1,2})T([^"]*?)")',
        r'Date.UTC(\g<year>, \g<month>, \g<day>)',
        series_json)

    return render_template(
        'index.html',
        title=u'Pengar',
        series=series_json
    )

@app.route('/update')
def update():
    return render_template(
        'update.html',
        title=u'Update'
    )
