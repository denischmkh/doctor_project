from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from parser_app.models import Doctor, Specialisation



def index(request: HttpRequest):
    specializations = Specialisation.objects.all()
    return render(request, 'base.html', context={
        "specializations": specializations,
    })


def get_doctors_by_specialisation(request: HttpRequest, specialization, page=1):
    doctors = Doctor.objects.filter(specialisations__name=specialization).order_by('name')
    paginator = Paginator(doctors, 24)  # 10 докторов на странице
    page_obj = paginator.get_page(page)
    print(specialization)
    print(doctors)

    return render(request, 'list_place.html', {
        'doctors': page_obj,
        'specialisation': specialization,
        'paginator': paginator,
    })
