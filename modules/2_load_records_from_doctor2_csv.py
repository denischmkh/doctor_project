import ast
import csv
import json
import os
import sys

from django.db import DataError

from load_django import *
from parser_app.models import *
from pathlib import Path

path = os.path.join(os.getcwd(), '..', 'files', 'doctors2')





files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in files:
    file_path = os.path.join(path, file)
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pprint(row)
            try:
                new_doctor, created = Doctor.objects.get_or_create(
                    name=row.get('first_name') + row.get('last_name'),
                    gender=row.get('gender'),
                    address=row.get('address_line_1'),
                    city=row.get('city'),
                    phone=row.get('phone'),
                )

                # Создание или извлечение объекта Education
                education = Education.objects.create(info=row.get('medical_school_name') if row.get('medical_school_name') != 'Other' else None)

                # Добавление Education в many-to-many связь
                new_doctor.educations.add(education)

                # Создание объекта Specialisation
                specialization = Specialisation.objects.create(name=row.get('doc_type'))

                # Добавление Specialisation в many-to-many связь
                new_doctor.specialisations.add(specialization)

                # Проверка и обработка locations_list, если он не пуст
                locations = row.get('locations_list')
                all_locations = []
                try:
                    data = ast.literal_eval(locations)  # Преобразуем строку в список Python
                except (ValueError, SyntaxError) as e:
                    print(f"Ошибка при парсинге строки: {e}")
                    data = []

                # Преобразование данных в объекты Hospital и сохранение в базу данных
                for entry in data:
                    # Извлекаем название больницы из addressLine2 или по умолчанию 'Unknown Hospital'
                    hospital_name = entry.get('addressLine2', 'Unknown Hospital')

                    # Создаем и сохраняем объект Hospital
                    hospital = Hospital.objects.create(name=hospital_name)
                    all_locations.append(hospital)
                new_doctor.hospitals.set(all_locations)
                new_doctor.save()
                print(f'{new_doctor.name} has been saved')

            except DataError:
                "Неподходящее значение"
                continue
