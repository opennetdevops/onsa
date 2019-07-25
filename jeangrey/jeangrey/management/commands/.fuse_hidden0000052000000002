from django.core.management.base import BaseCommand
import csv
import os
from jeangrey.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(base + "/legacy_services.csv", mode='r') as csv_file:
            dialect = csv.excel()
            dialect.delimiter = ';'
            csv_reader = csv.DictReader(csv_file, dialect=dialect)
            # First pass, normalize clients
            for row in csv_reader:
                try:
                    client = Client.objects.get(cuic=row["CUIT"])
                except Client.MultipleObjectsReturned as e:
                    print(
                        f'deleting remaining entries due to CUIT:{row["CUIT"]} and {e}')
                    to_delete = Client.objects.filter(cuic=row["CUIT"])
                    i = 1
                    while i < len(to_delete):
                        to_delete[i].delete()
                        i += 1
                except Client.DoesNotExist:
                    print(
                        f'Going to add since it doesnt exists: {row["CUIT"]}, {row["Name"]}')
                    a = Client(cuic=row["CUIT"], name=row["Name"])
                    a.save()

                # Create customer location
                cust_loc = CustomerLocation(
                    client=client, address=row["Device Location"])
                cust_loc.save()
                # Create service
                svc = Legacy(client=client, customer_location=cust_loc,
                              id=row['Prod_ID'], client_node_sn=row["Serial Number"], service_state="service_activated", service_type="legacy")
                svc.save()
