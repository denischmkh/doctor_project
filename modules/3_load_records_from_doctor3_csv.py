import ast
import csv
import json
import os

from django.core.management import BaseCommand
from django.db import DataError

from load_django import *
from parser_app.models import *
from pathlib import Path

csv_filepath = os.path.join(os.getcwd(), '..', 'files', 'doctors3', 'doctors.csv')


def import_doctors_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            doctor_data = {
                'name': f"{row.get('Provider First Name', '')} {row.get('Provider Last Name', '')}".strip(),
                'gender': row.get('Provider Gender Code'),
                'city': row.get('Provider Business Mailing Address City Name'),
                'address': row.get('Provider Business Mailing Address'),
                'phone': row.get('Provider Business Mailing Address Telephone Number'),
                'email': row.get('Provider Email'),
                'site_url': row.get('Provider Business Practice Location Address'),
            }

            # Проверяем, существует ли врач в базе
            doctor, created = Doctor.objects.get_or_create(name=doctor_data['name'], defaults=doctor_data)

            if created:
                print(f'{doctor} was created')
            else:
                print(f'{doctor} already existed')

            languages = row.get('Provider Languages', '').split(',')  # допустим, языки перечислены через запятую
            for lang in languages:
                language, created = Language.objects.get_or_create(name=lang.strip())
                doctor.languages.add(language)

            # Пример с больницами
            hospitals = row.get('Provider Hospitals', '').split(',')
            for hospital_name in hospitals:
                hospital, created = Hospital.objects.get_or_create(name=hospital_name.strip())
                doctor.hospitals.add(hospital)

            # Пример с специализациями
            specialisations = row.get('Provider Specialisation', '').split(',')
            for specialisation_name in specialisations:
                specialisation, created = Specialisation.objects.get_or_create(name=specialisation_name.strip())
                doctor.specialisations.add(specialisation)

            # Сохранить изменения
            doctor.save()


# 🔹 Запуск скрипта
if __name__ == "__main__":
    import_doctors_from_csv(str(csv_filepath))