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

    # Создаем слаги для каждой специализации
    specializations_with_slugs = []
    for specialization in specializations:
        slug = string_to_slug(specialization.name)
        specializations_with_slugs.append({
            'name': specialization.name,
            'slug': slug,
        })

    # Передаем данные в шаблон
    return render(request, 'base.html', context={
        "specializations": specializations_with_slugs,
    })


def get_doctors_by_specialisation(request, specialization_slug, page=1):
    # Преобразуем слаг обратно в объект специализации
    try:
        specialization = Specialisation.objects.get(slug=specialization_slug)
    except Specialisation.DoesNotExist:
        return render(request, 'error.html', {'message': 'Специализация не найдена!'})

    # Получаем список докторов, у которых есть соответствующая специализация с нужным слагом
    doctors = Doctor.objects.filter(specialisations__slug=specialization_slug).order_by('name')
    paginator = Paginator(doctors, 24)  # Например, 24 доктора на странице
    page_obj = paginator.get_page(page)

    return render(request, 'list_place.html', {
        'doctors': page_obj,
        'specialisation': specialization,
        'paginator': paginator,
    })
