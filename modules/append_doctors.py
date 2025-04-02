import random
from load_django import *
from parser_app.models import Clinic, Doctor, Language, Hospital, Specialisation, Education, WorkExperience, \
    Apprenticeship, Publication, Research, Award, Competence, Membership
from faker import Faker  # Используем библиотеку Faker для генерации случайных данных

# Инициализация Faker
fake = Faker()

# 1. Получить или создать клинику
clinic_name = "Jamesburg Clincs"  # Название клиники
clinic, created = Clinic.objects.get_or_create(title=clinic_name, location="Some Location",
                                               image="https://example.com/image.jpg")

# 2. Создать связанные объекты (например, языки, больницы, специализации и т. д.)
# Создаем примерный список языков, больниц, специализаций и т. д.
languages = [Language.objects.create(name=f"Language {i}") for i in range(1, 6)]
hospitals = [Hospital.objects.create(name=f"Hospital {i}") for i in range(1, 6)]
specialisations = [Specialisation.objects.create(name=f"Specialisation {i}") for i in range(1, 6)]
educations = [Education.objects.create(info=f"Education {i}", year=str(2000 + i)) for i in range(1, 6)]
work_experience = [WorkExperience.objects.create(info=f"Work Experience {i}", year=str(2000 + i)) for i in range(1, 6)]
apprenticeships = [Apprenticeship.objects.create(info=f"Apprenticeship {i}", year=str(2000 + i)) for i in range(1, 6)]
publications = [Publication.objects.create(title=f"Publication {i}", year=str(2000 + i)) for i in range(1, 6)]
researches = [Research.objects.create(title=f"Research {i}", year=str(2000 + i)) for i in range(1, 6)]
awards = [Award.objects.create(name=f"Award {i}", year=str(2000 + i)) for i in range(1, 6)]
competences = [Competence.objects.create(name=f"Competence {i}") for i in range(1, 6)]
memberships = [Membership.objects.create(name=f"Membership {i}") for i in range(1, 6)]

# 3. Создание докторов и их связей
for i in range(1, 21):  # Создаем 20 докторов
    name = fake.name()  # Генерируем случайное имя
    description = fake.sentence()  # Генерируем случайное описание
    profile_url = fake.url()  # Генерируем случайный URL
    phone = fake.phone_number()  # Генерируем случайный номер телефона
    email = fake.email()  # Генерируем случайный email
    vcard_url = fake.url()  # Генерируем случайный vCard URL
    cv_url = fake.url()  # Генерируем случайный CV URL
    photo_url = fake.image_url()  # Генерируем случайный URL для фото
    gender = random.choice(["M", "F"])  # Случайный выбор пола
    city = fake.city()  # Генерируем случайный город
    address = fake.address()  # Генерируем случайный адрес
    fax = fake.phone_number()  # Генерируем случайный номер факса
    instagram = fake.url()  # Генерируем случайный Instagram URL
    facebook = fake.url()  # Генерируем случайный Facebook URL
    twitter = fake.url()  # Генерируем случайный Twitter URL
    linkedin = fake.url()  # Генерируем случайный LinkedIn URL
    youtube = fake.url()  # Генерируем случайный YouTube URL
    site_url = fake.url()  # Генерируем случайный сайт URL
    media_urls = {"media": [fake.image_url()]}  # Генерируем случайные медиа URL

    # Создаем доктора
    doctor = Doctor.objects.create(
        name=name,
        description=description,
        profile_url=profile_url,
        phone=phone,
        email=email,
        vcard_url=vcard_url,
        cv_url=cv_url,
        photo_url=photo_url,
        gender=gender,
        city=city,
        address=address,
        fax=fax,
        instagram=instagram,
        facebook=facebook,
        twitter=twitter,
        linkedin=linkedin,
        youtube=youtube,
        site_url=site_url,
        media_urls=media_urls
    )

    # Присваиваем связи с клиникой и другими моделями
    doctor.clinic.add(clinic)

    # Присваиваем случайные связанные данные
    doctor.languages.set(random.sample(languages, 3))  # Присваиваем 3 случайных языка
    doctor.hospitals.set(random.sample(hospitals, 2))  # Присваиваем 2 случайных больницы
    doctor.specialisations.set(random.sample(specialisations, 1))  # Присваиваем 1 случайную специализацию
    doctor.educations.set(random.sample(educations, 1))  # Присваиваем 1 случайное образование
    doctor.work_experience.set(random.sample(work_experience, 1))  # Присваиваем 1 случайный опыт работы
    doctor.apprenticeships.set(random.sample(apprenticeships, 1))  # Присваиваем 1 случайную стажировку
    doctor.publications.set(random.sample(publications, 1))  # Присваиваем 1 случайную публикацию
    doctor.researches.set(random.sample(researches, 1))  # Присваиваем 1 случайное исследование
    doctor.awards.set(random.sample(awards, 1))  # Присваиваем 1 случайную награду
    doctor.competences.set(random.sample(competences, 1))  # Присваиваем 1 случайную компетенцию
    doctor.memberships.set(random.sample(memberships, 1))  # Присваиваем 1 случайное членство

    doctor.save()

print("20 doctors created with diverse random data and related models.")