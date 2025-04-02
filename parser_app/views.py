import json
import urllib
from urllib.parse import urlencode

from django import template
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Doctor, Specialisation, Language, Clinic


necessary_specializations = ['Oral surgery', 'Physiologi', 'Paediatrics', 'Infectiology', 'Neurologie', 'Urologie',
                             'Andrology', 'Neurosurgery', 'Oralchirurgie', 'Proctology', 'Pathology', 'Radiologi',
                             'Diabetology', 'Urogynaecology', 'Hematology', 'Neuropsychology', 'Rheumatology',
                             'Lymphology', 'MRI', 'Cataracts', 'Spinal surgery', 'Hernias',
                             'Sportmedizin', 'arodontologie', 'Neuropathologi', 'Mikrobiologie', 'Cardiology',
                             'Ultraschall', 'Endocrinology', 'Eye surgery', 'Orthopädie']


genders = {
        'M': 'Male',
        'F': 'Female',
    }

def doctor_list(request: HttpRequest, page=1) :
    if request.method == 'GET':
        selected_filters = request.GET.getlist('filter')
        per_page = 10
        end = page * per_page
        start = end - per_page
        if start == 0:
            previous_page = None
        else:
            previous_page = page - 1

        query = Q()

        # Если выбран хотя бы один фильтр, формируем условия для фильтрации
        if selected_filters:
            # Добавляем фильтры для специализаций
            query |= Q(specialisations__name__in=selected_filters)

            # Добавляем фильтры для языков
            query |= Q(languages__name__in=selected_filters)

            # Добавляем фильтры для гендера
            query |= Q(gender__in=selected_filters)

        # Применяем фильтрацию с комбинированными условиями
        doctors = Doctor.objects.filter(query).distinct()



        if len(doctors) < per_page - 1:
            next_page = None
        else:
            next_page = page + 1

        doctors_count = len(doctors)

        languages = [el.name for el in Language.objects.all()]

        query_params = [('filter', value) for value in selected_filters]
        query_string = urlencode(query_params, doseq=True)

        return render(request, 'search-2.html', {'doctors': doctors[start:end],
                                                 'doctors_count': doctors_count,
                                                 'previous_page': previous_page,
                                                 'next_page': next_page,
                                                 'page': page,
                                                 'selected_filters': selected_filters,
                                                 'specializations': necessary_specializations,
                                                 'languages': languages,
                                                 'genders': genders,
                                                 'query_string': query_string})


def doctor_profile(request, id: int):
    doctor = get_object_or_404(Doctor, id=id)
    awards_count = doctor.awards.count()
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
    else:
        pass
    specialisations = doctor.specialisations.all()
    memberships = doctor.memberships.all()
    awards = doctor.awards.all()
    main_speciality = specialisations[0]

    print(doctor.work_experience.all())
    return render(request, 'doctor-profile.html', {'doctor': doctor,
                                                   'awards_count': awards_count,
                                                   'working_from': min(years_experience) if years_experience else None,
                                                   'specialisations': specialisations,
                                                   'memberships': memberships,
                                                   'main_speciality': main_speciality,
                                                   'awards': awards})


def select_filters(request: HttpRequest):
    if request.method == 'POST':
        # Получаем все значения из POST-запроса
        params = list(request.POST.values())
        # Если только одно значение, просто редиректим
        if len(params) == 1:
            response = HttpResponseRedirect(reverse('doctor_list'))
            return response

        # Формируем список фильтров с одинаковым именем "filter"
        query_params = [('filter', value) for value in params]

        # Преобразуем их в строку query параметров
        query_string = urlencode(query_params, doseq=True)

        # Формируем URL с добавлением query строки
        url = f"{reverse('doctor_list')}?{query_string}"

        # Переадресовываем на новый URL с query параметрами
        return HttpResponseRedirect(url)


def get_clinics(request: HttpRequest, page=1):
    if request.method == 'GET':
        clinics = Clinic.objects.all()

        per_page = 9
        end = page * per_page
        start = end - per_page

        previous_page = page - 1 if start > 0 else None

        next_page = page + 1 if end < len(clinics) else None


        doctors_count_with_clinic = {clinic: len(Doctor.objects.filter(clinic__title=clinic.title)) for clinic in clinics[start:end]}


        return render(request, 'clinic.html', {
            "clinics_count": len(clinics),
            "previous_page": previous_page,
            "page": page,
            "next_page": next_page,
            'doctors_count_with_clinic': doctors_count_with_clinic
        })



def get_doctor_grid(request: HttpRequest, clinic, page=1):
    selected_filters = request.GET.getlist('filter')
    doctors = Doctor.objects.filter(clinic__title=clinic)  # Получаем врачей только из этой клиники
    per_page = 12
    end = page * per_page
    start = end - per_page
    previous_page = page - 1 if start > 0 else None
    next_page = page + 1 if end < len(doctors) else None

    languages = [el.name for el in Language.objects.all()]

    if selected_filters:
        query = Q()

        # Добавляем фильтры ТОЛЬКО к уже найденным врачам
        query |= Q(specialisations__name__in=selected_filters)
        query |= Q(languages__name__in=selected_filters)
        query |= Q(gender__in=selected_filters)

        # Применяем фильтры к уже выбранным врачам
        doctors = doctors.filter(query).distinct()

    return render(request, 'doctor-grid.html', {
        'doctors_count': len(doctors),
        'doctors': doctors[start:end],
        'clinic': clinic,
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'languages': languages,
        'specializations': necessary_specializations,
        'genders': genders,
    })

def select_filters_from_grid(request: HttpRequest):
    if request.method == 'POST':

        params = list(request.POST.values())
        # Если только одно значение, просто редиректим
        if len(params) == 1:
            response = HttpResponseRedirect(reverse('get_doctor_grid'))
            return response

        # Формируем список фильтров с одинаковым именем "filter"
        query_params = [('filter', value) for value in params]

        # Преобразуем их в строку query параметров
        query_string = urlencode(query_params, doseq=True)

        # Формируем URL с добавлением query строки
        url = f"{reverse('get_doctor_grid')}?{query_string}"
        clinic = request.POST.get('clinic', 'default_clinic_name')
        page = request.POST.get('page', 1)

        response = HttpResponseRedirect(reverse('get_doctor_grid', args=[clinic, page]))
        return HttpResponseRedirect(url)