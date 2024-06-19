# management/commands/load_instruments.py
import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Instrument

class Command(BaseCommand):
    help = 'Load instruments from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'complete.csv'

        # Delete all existing instruments
        Instrument.objects.all().delete()

        instruments = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instruments.append(Instrument(
                    instrument_key=row['instrument_key'],
                    exchange_token=row['exchange_token'] if row['exchange_token'] else None,
                    tradingsymbol=row['tradingsymbol'] if row['tradingsymbol'] else None,
                    name=row['name'],
                    last_price=float(row['last_price']) if row['last_price'] else None,
                    expiry=row['expiry'] if row['expiry'] else None,
                    strike=float(row['strike']) if row['strike'] else None,
                    tick_size=float(row['tick_size']) if row['tick_size'] else None,
                    lot_size=int(row['lot_size']) if row['lot_size'] else None,
                    instrument_type=row['instrument_type'],
                    option_type=row['option_type'] if row['option_type'] else None,
                    exchange=row['exchange'],
                ))

        # Bulk create all instruments in a single transaction
        with transaction.atomic():
            Instrument.objects.bulk_create(instruments, batch_size=1000)

        self.stdout.write(self.style.SUCCESS('Successfully loaded instruments'))
