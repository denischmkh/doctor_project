from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.text import slugify
from parser_app.models import Doctor, Specialisation

specialization_map = {}


def string_to_slug(original_string: str):
    # Преобразуем строку в слаг
    slug = slugify(original_string)
    # Сохраняем в словарь (или базу данных)
    specialization_map[slug] = original_string
    return slug


def slug_to_string(slug: str):
    # Получаем оригинальное значение по слагу
    return specialization_map.get(slug, None)


def index(request: HttpRequest):
    # Получаем все специализации
    specializations = Specialisation.objects.all()

    # Передаем данные в шаблон
    return render(request, 'index.html', context={
        "specializations": specializations,
    })


def get_doctors_by_specialisation(request: HttpRequest, specialization_slug, page=1):

    try:
        specialization = Specialisation.objects.get(slug=specialization_slug)
    except Specialisation.DoesNotExist:
        return render(request, 'error.html', {'message': 'Специализация не найдена!'})

    # Получаем список докторов, у которых есть соответствующая специализация с нужным слагом
    doctors = Doctor.objects.filter(specialisations__slug=specialization_slug).order_by('name')

    filters = request.GET.dict()
    selected_source = filters.get('source')
    if selected_source:
        doctors = doctors.filter(source=selected_source)
    paginator = Paginator(doctors, 24)  # Например, 24 доктора на странице
    page_obj = paginator.get_page(page)
    unique_sources = Doctor.objects.values_list('source', flat=True).distinct().order_by('source')

    return render(request, 'list_doctors.html', {
        'doctors': page_obj,
        'specialization_slug': specialization_slug,
        'paginator': paginator,
        'sources': unique_sources,
        'selected_category_name': Specialisation.objects.filter(slug=specialization_slug).first().name,
        'selected_category': specialization_slug,
    })


def get_profile(request: HttpRequest, id: int):
    doctor = Doctor.objects.filter(id=id).first()

    years_experience = []
    work_experience = doctor.work_experience.all()
    if work_experience:
        for experience in work_experience:
            year_str = experience.year
            digits = []
            for el in year_str:
                if el.isdigit():
                    digits.append(el)
            years_experience.append(int("".join(digits)))

    awards_count = doctor.awards.count()

    context = {
        'doctor': doctor,
        'working_from': min(years_experience) if years_experience else None,
        'awards_count': awards_count,
        'has_awards': bool(awards_count),
        'selected_category_name': doctor.specialisations.first().name,
        'selected_category': doctor.specialisations.first().slug,
        'name': doctor.name
    }
    return render(request, 'doctor_profile.html', context=context)