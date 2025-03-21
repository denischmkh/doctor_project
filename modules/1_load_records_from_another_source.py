import csv
import os
from load_django import *
from parser_app.models import *
from pathlib import Path

path = os.path.join(os.getcwd(), '..', 'files', 'doctors')

files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

r = 1

for file in files:
    file_path = os.path.join(path, file)
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_doctor = Doctor.objects.get_or_create(
                name=row.get('doctor_name', None) if row.get('doctor_name') != "NULL" else None,
                profile_url=row.get('doctor_link', None) if row.get('doctor_link') != "NULL" else None,
                address=row.get('address', None) if row.get('address') != "NULL" else None,
                phone=row.get('phone')[3:-2] if row.get('phone') != "NULL" else None,
                fax=row.get('fax') if row.get('fax') != "NULL" else None,
                site_url=row.get('website') if row.get('website') != "NULL" else None,
                email=row.get('doctor_email')[3:-2].split(",")[0] if row.get('doctor_email') != "NULL" else None,
                instagram=row.get('doctor_instagram', None)[1:-1] if row.get('doctor_instagram') != "NULL" else None,
                facebook=row.get('doctor_facebook', None)[1:-1] if row.get('doctor_facebook') != "NULL" else None,
                twitter=row.get('doctor_twitter', None)[1:-1] if row.get('doctor_twitter') != "NULL" else None,
                linkedin=row.get('doctor_linkedin', None)[1:-1] if row.get('doctor_linkedin') != "NULL" else None,
                youtube=row.get('doctor_youtube', None)[1:-1] if row.get('doctor_youtube') != "NULL" else None,
            )

            # Обработка specialties
            specialties = []
            try:
                for specialty in row.get('specialty')[3:-2].split(',') if row.get('specialty') != "NULL" else None:
                    try:
                        spec = Specialisation(name=specialty)
                    except AttributeError:
                        break
                    spec.save()
                    specialties.append(spec)
                try:
                    new_doctor.specialisations.set(specialties)
                    new_doctor.save()
                except AttributeError:
                    continue
                print(r)
                r += 1
            except TypeError:
                continue
