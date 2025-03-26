import csv
import os
import ast
from load_django import *
from parser_app.models import *

def parse_json_field(field_value):
    try:
        return ast.literal_eval(field_value) if field_value != 'NULL' else []
    except (ValueError, SyntaxError):
        return []


path = os.path.join(os.getcwd(), '..', 'files', 'parser_app_doctor.csv')
with open(str(path), mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rw = 0
    for row in reader:
        languages = parse_json_field(row.get('languages', None))
        hospitals = parse_json_field(row.get('hospitals', None))
        specialisations = parse_json_field(row.get('specialisations', None))
        specialisations.append(parse_json_field(row.get('specialty', None)))
        educations = parse_json_field(row.get('educations', None))
        work_experience = parse_json_field(row.get('work_experiences', None))
        apprenticeships = parse_json_field(row.get('apprenticeships', None))
        publications = parse_json_field(row.get('publications', None))
        researches = parse_json_field(row.get('researches', None))
        awards = parse_json_field(row.get('awards', None))
        competences = parse_json_field(row.get('competences', None))
        memberships = parse_json_field(row.get('memberships', None))

        address = parse_json_field(row.get('address', None))
        fax = parse_json_field(row.get('fax', None))
        instagram = parse_json_field(row.get('instagram', None))
        facebook = parse_json_field(row.get('facebook', None))
        twitter = parse_json_field(row.get('twitter', None))
        linkedin = parse_json_field(row.get('linkedin', None))
        youtube = parse_json_field(row.get('youtube', None))


        language_objects = []
        for language in languages:
            if language:
                language_obj, created = Language.objects.get_or_create(name=language)
                language_objects.append(language_obj)

        hospital_objects = []
        for hospital in hospitals:
            if hospital:
                hospital_obj, created = Hospital.objects.get_or_create(name=hospital)
                hospital_objects.append(hospital_obj)

        specialisation_objects = []
        for specialisation in specialisations:
            if specialisation:
                specialisation_obj, created = Specialisation.objects.get_or_create(name=specialisation)
                specialisation_objects.append(specialisation_obj)

        education_objects = []
        for education in educations:
            if isinstance(education, dict):
                info = education.get('info')
                year = education.get('year')
                if info:
                    education_obj, created = Education.objects.get_or_create(info=info, year=year)
                    education_objects.append(education_obj)

        work_experience_objects = []
        for work in work_experience:
            if isinstance(work, dict):
                info = work.get('info')
                year = work.get('year')
                if info:
                    work_experience_obj, created = WorkExperience.objects.get_or_create(info=info, year=year)
                    work_experience_objects.append(work_experience_obj)

        apprenticeship_objects = []
        for apprenticeship in apprenticeships:
            if apprenticeship:
                apprenticeship_obj, created = Apprenticeship.objects.get_or_create(info=apprenticeship)
                apprenticeship_objects.append(apprenticeship_obj)

        publication_objects = []
        for publication in publications:
            if isinstance(publication, dict):
                title = publication.get('title')
                year = publication.get('year')
                if title and year:
                    publication_obj, created = Publication.objects.get_or_create(title=title, year=year)
                    publication_objects.append(publication_obj)
                elif title:
                    publication_obj, created = Publication.objects.get_or_create(title=title)
                    publication_objects.append(publication_obj)
                elif year:
                    publication_obj, created = Publication.objects.get_or_create(year=year)
                    publication_objects.append(publication_obj)

        research_objects = []
        for research in researches:
            if isinstance(research, str):  # Если research — это строка
                title = research
                research_obj, created = Research.objects.get_or_create(title=title)
                research_objects.append(research_obj)
            elif isinstance(research, dict):  # Если research — это словарь
                title = research.get('title')
                year = research.get('year')
                if title and year:
                    research_obj, created = Research.objects.get_or_create(title=title, year=year)
                    research_objects.append(research_obj)
                elif title:
                    research_obj, created = Research.objects.get_or_create(title=title)
                    research_objects.append(research_obj)
                elif year:
                    research_obj, created = Research.objects.get_or_create(year=year)
                    research_objects.append(research_obj)

        award_objects = []
        for award in awards:
            items = award.get('items', [])
            for item in items:
                parts = item.split(",")
                if len(parts) > 1:
                    name = parts[0].strip()
                    year = parts[-1].strip()
                    if name:
                        award_obj, created = Award.objects.get_or_create(name=name, year=year)
                        award_objects.append(award_obj)

        competence_objects = []
        for competence in competences:
            if competence:
                competence_obj, created = Competence.objects.get_or_create(name=competence)
                competence_objects.append(competence_obj)

        membership_objects = []
        for membership in memberships:
            if membership:
                membership_obj, created = Membership.objects.get_or_create(name=membership)
                membership_objects.append(membership_obj)
        try:
            doctor_obj, created = Doctor.objects.get_or_create(
                name=row.get('name') or row.get('doctor_name'),
                clinic=row.get('clinic'),
                description=row.get('description'),
                profile_url=row.get('profile_url') or row.get('doctor_link'),
                phone=row.get('phone')[3:-2],
                email=row.get('email')[2:-1],
                vcard_url=row.get('vcard_url'),
                address=row.get('address') if row.get('address') not in ['NULL', None] else None,
                fax=row.get('fax') if row.get('fax') not in ['NULL', None] else None,
                cv_url=row.get('cv_url'),
                photo_url=row.get('photo_url'),
                site_url=row.get('site_url') if row.get('site_url') not in ['NULL', None] else None,
                media_urls=row.get('media_urls') if row.get('media_urls') not in ['NULL', None] else None,
                instagram=row.get('doctor_instagram') if row.get('doctor_instagram') not in ['NULL', None] else None,
                facebook=row.get('doctor_facebook') if row.get('doctor_facebook') not in ['NULL', None] else None,
                twitter=row.get('doctor_twitter') if row.get('doctor_twitter') not in ['NULL', None] else None,
                linkedin=row.get('doctor_linkedin') if row.get('doctor_linkedin') not in ['NULL', None] else None,
                youtube=row.get('doctor_youtube') if row.get('doctor_youtube') not in ['NULL', None] else None,
            )
        except Exception as e:
            print(e)
            continue

        doctor_obj.languages.set(language_objects)
        doctor_obj.hospitals.set(hospital_objects)
        doctor_obj.specialisations.set(specialisation_objects)
        doctor_obj.educations.set(education_objects)
        doctor_obj.work_experience.set(work_experience_objects)
        doctor_obj.apprenticeships.set(apprenticeship_objects)
        doctor_obj.publications.set(publication_objects)
        doctor_obj.researches.set(research_objects)
        doctor_obj.awards.set(award_objects)
        doctor_obj.competences.set(competence_objects)
        doctor_obj.memberships.set(membership_objects)

        doctor_obj.save()
        rw += 1
        print(rw)
        print(f"Doctor '{doctor_obj.name}' has been created/updated. from file {file.name}")

