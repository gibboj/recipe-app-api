import time

from django.db import connections
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until db is available"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                sleeptime = 1
                self.stdout.write(
                    "Database unavailable, waiting %s second..." % sleeptime
                )
                time.sleep(sleeptime)
        self.stdout.write(self.style.SUCCESS("Database available"))
