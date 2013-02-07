from mig import run
from mig.models import MigrationData

from pengar import database, models, migrations

db = database.db

def main():
    run(db.engine, u'__main__', models.MODELS, migrations.MIGRATIONS)
