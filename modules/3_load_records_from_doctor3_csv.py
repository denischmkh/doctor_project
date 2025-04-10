import ast
import csv
import json
import os

from django.core.management import BaseCommand
from django.db import DataError
from taxonomy_keys import taxonomy_keys

from load_django import *
from parser_app.models import *
from pathlib import Path

csv_filepath = os.path.join(os.getcwd(), '..', 'files', 'doctors3', 'doctors.csv')


def import_doctors_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row.get('Healthcare Provider Taxonomy Group_1'))
            if not row.get('Provider First Name'):
                continue
            doctor_data = {
                'name': f"{row.get('Provider First Name', '')} {row.get('Provider Middle Name')} {row.get('Provider Last Name (Legal Name)', '')}".strip(),
                'city': row.get('Provider Business Practice Location Address City Name'),
                'postcode': row.get('Provider Business Practice Location Address Postal Code'),
                'gender': row.get('Provider Gender Code'),
                'address': f"{row.get('Provider Business Practice Location Address State Name')} {row.get('Provider Business Practice Location Address City Name')}",
                'phone': row.get('Provider Business Practice Location Address Telephone Number'),
                'fax': row.get('Provider Business Practice Location Address Fax Number'),
                'description': row.get('Provider Credential Text'),
                'source': 'nppes.cms.hhs.gov'
            }

            # Проверяем, существует ли врач в базе
            doctor, created = Doctor.objects.get_or_create(name=doctor_data['name'], defaults=doctor_data)
            if created:
                print(f'{doctor} was created')
            else:
                print(f'{doctor} already existed')

            clinic, created = Clinic.objects.get_or_create(title=row.get('Provider Organization Name (Legal Business Name)'))
            doctor.clinic.add(clinic)
            try:
                specialisation, created = Specialisation.objects.get_or_create(name=taxonomy_keys[row.get('Healthcare Provider Taxonomy Group_1').split(' ')[0]])
                doctor.specialisations.add(specialisation)
            except KeyError:
                print('Key not found!')
                pass
            doctor.save()
            print(f'{doctor.name} has been saved')





# 🔹 Запуск скрипта
if __name__ == "__main__":
    import_doctors_from_csv(str(csv_filepath))