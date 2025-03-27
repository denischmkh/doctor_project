import json
import urllib

from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Doctor, Specialisation, Language


necessary_specializations = ['Oral surgery', 'Physiologi', 'Paediatrics', 'Infectiology', 'Neurologie', 'Urologie',
                             'Andrology', 'Neurosurgery', 'Oralchirurgie', 'Proctology', 'Pathology', 'Radiologi',
                             'Diabetology', 'Urogynaecology', 'Hematology', 'Neuropsychology', 'Rheumatology',
                             'Lymphology', 'MRI', 'Cataracts', 'Spinal surgery', 'Hernias',
                             'Sportmedizin', 'arodontologie', 'Neuropathologi', 'Mikrobiologie', 'Cardiology',
                             'Ultraschall', 'Endocrinology', 'Eye surgery', 'Orthopädie']


genders = ['M', 'F']

def doctor_list(request: HttpRequest, page=1) :
    if request.method == 'GET':
        selected_filters = request.GET.getlist('filter')
        print(selected_filters)
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

        return render(request, 'search-2.html', {'doctors': doctors[start:end],
                                                 'doctors_count': doctors_count,
                                                 'previous_page': previous_page,
                                                 'next_page': next_page,
                                                 'page': page,
                                                 'selected_filters': selected_filters,
                                                 'specializations': necessary_specializations,
                                                 'languages': languages,
                                                 'genders': genders})


def doctor_profile(request, id: int):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'doctor-profile-2.html', {'doctor': doctor})


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
        query_string = urllib.parse.urlencode(query_params, doseq=True)

        # Формируем URL с добавлением query строки
        url = f"{reverse('doctor_list')}?{query_string}"

        # Переадресовываем на новый URL с query параметрами
        return HttpResponseRedirect(url)

