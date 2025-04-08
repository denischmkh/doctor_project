from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from parser_app.models import Doctor, Specialisation

specializations = ['Oral surgery', 'Physiologi', 'Paediatrics', 'Infectiology', 'Neurologie', 'Urologie',
                             'Andrology', 'Neurosurgery', 'Oralchirurgie', 'Proctology', 'Pathology', 'Radiologi',
                             'Diabetology', 'Urogynaecology', 'Hematology', 'Neuropsychology', 'Rheumatology',
                             'Lymphology', 'MRI', 'Cataracts', 'Spinal surgery', 'Hernias',
                             'Sportmedizin', 'arodontologie', 'Neuropathologi', 'Mikrobiologie', 'Cardiology',
                             'Ultraschall', 'Endocrinology', 'Eye surgery', 'Orthopädie']

def index(request: HttpRequest):
    print(specializations)
    return render(request, 'base.html', context={
        "specializations": specializations,
    })


def get_doctors_by_specialisation(request: HttpRequest, specialisation: str, page=1):
    specialisation_obj = Specialisation.objects.filter(name=specialisation).first()

    # Если не найдено подходящей специализации, возвращаем пустой список
    if not specialisation_obj:
        doctors = Doctor.objects.none()  # Пустой queryset
    else:
        # Получаем всех докторов, у которых есть соответствующая специализация
        doctors = Doctor.objects.filter(specialisations=specialisation_obj)

    paginator = Paginator(doctors, 24)  # 10 докторов на странице
    page_obj = paginator.get_page(page)
    print(specialisation)
    print(doctors)

    return render(request, 'list_place.html', {
        'doctors': page_obj,
        'specialisation': specialisation,
    })
