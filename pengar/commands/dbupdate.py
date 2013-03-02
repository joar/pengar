from mig import run
from mig.models import MigrationData

from pengar import database, models, migrations
from pengar.www import models as wwwmodels
from pengar.www import migrations as wwwmigrations

db = database.db

def main():
    run(db.engine, u'__main__', models.MODELS, migrations.MIGRATIONS)
    run(db.engine, u'www', wwwmodels.MODELS, wwwmigrations.MIGRATIONS)
