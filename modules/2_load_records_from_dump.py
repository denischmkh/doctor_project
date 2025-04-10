import ast
import csv
import json
import os
import re
import sys

import psycopg2
from django.db import DataError

from load_django import *
from parser_app.models import *
from pathlib import Path

connection = psycopg2.connect(
    dbname="doctors_dump",
    user="postgres",
    password="denis2004",
    host="localhost"
)

cursor = connection.cursor()


query = """SELECT * FROM parser_app_doctor LIMIT 800;"""
cursor.execute(query)

# Теперь cursor.description уже доступен
column_names = [desc[0] for desc in cursor.description]

# Получение всех строк из таблицы
rows = cursor.fetchall()

for row in rows:
    row_dict = dict(zip(column_names, row))
    # pprint(row_dict)

    doctor, created = Doctor.objects.get_or_create(
        name=f"{row_dict['first_name']} {row_dict['last_name']}",
        phone=row_dict.get('phone'),
        gender=row_dict.get('gender'),
        city=row_dict.get('city'),
        address=row_dict.get('address_line_1'),
        postcode=row_dict.get('zipcode'),
        source='medicare.gov'
    )

    # Создаем или находим образование
    education, created = Education.objects.get_or_create(
        info=row_dict.get('medical_school_name'),
        year=row_dict.get('graduation_year'),
    )

    # Создаем или находим клинику
    clinic, created = Clinic.objects.get_or_create(
        title=row_dict.get('main_organization_name'),
    )


    specialties_str = row_dict.get('specialties_list')
    if specialties_str != '[]':
        specialties_str = specialties_str.replace("'", '"')  # Заменяем одинарные кавычки на двойные
        specialties_str = specialties_str.replace(r'\"', '"')  # Заменяем экранированные кавычки на обычные
        specialties_str = specialties_str.strip()
        parsed_list = specialties_str[specialties_str.index('{')+1:specialties_str.index('}}')].replace('"', '').replace("'", "").split(',')
        for el in parsed_list:
            if 'specialtyName' in el:
                print(el)
                specialisation, created = Specialisation.objects.get_or_create(
                    name=el.split(':')[1]
                )





    work_experiences_str = row_dict.get('group_affiliations_list')
    if work_experiences_str != '[]':
        print(work_experiences_str)
        work_experiences_str = work_experiences_str.replace("'", '"')  # Заменяем одинарные кавычки на двойные
        work_experiences_str = work_experiences_str.replace(r'\"', '"')  # Заменяем экранированные кавычки на обычные
        work_experiences_str = work_experiences_str.strip()
        parsed_list = work_experiences_str[work_experiences_str.index('{') + 1:work_experiences_str.index('}')].replace('"', '').replace("'", "").split(',')

        for el in parsed_list:
            if 'organizationName' in el:
                print(el)
                specialisation, created = WorkExperience.objects.get_or_create(
                    info=el.split(':')[1]
                )

    # Присваиваем клинику доктору
    doctor.clinic.add(clinic)

    # Присваиваем образование доктору
    doctor.educations.add(education)

    doctor.save()



