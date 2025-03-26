import json

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
        if request.COOKIES.get('selected_specializations'):
            selected_specializations = json.loads(request.COOKIES.get('selected_specializations'))
        else:
            selected_specializations = []
        if request.COOKIES.get('selected_languages'):
            selected_languages = json.loads(request.COOKIES.get('selected_languages'))
        else:
            selected_languages = []

        if request.COOKIES.get('selected_genders'):
            selected_genders = json.loads(request.COOKIES.get('selected_languages'))
        else:
            selected_genders = []

        unique_specializations = set()
        all_specializations = Specialisation.objects.all()
        for specialization in all_specializations:
            unique_specializations.add(specialization.name)



        per_page = 10
        end = page * per_page
        start = end - per_page
        if start == 0:
            previous_page = None
        else:
            previous_page = page - 1

        doctors = []

        if selected_specializations:
            for specialization in selected_specializations:
                spec = Specialisation.objects.filter(name=specialization).first()
                if spec:
                    doctors.extend(Doctor.objects.filter(specialisations=spec))

        if selected_genders:
            doctors = [doctor for doctor in doctors if doctor.gender in selected_genders]

        if selected_languages:
            doctors = [doctor for doctor in doctors if doctor.languages.filter(name__in=selected_languages).exists()]




        if not doctors:
            doctors = Doctor.objects.all()[start:end]



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
                                                 'specializations': necessary_specializations,
                                                 'selected_specializations': selected_specializations,
                                                 'selected_languages': selected_languages,
                                                 'selected_genders': selected_genders,
                                                 'languages': languages,
                                                 'genders': genders})


def doctor_profile(request, id: int):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'doctor-profile-2.html', {'doctor': doctor})


def select_specializations(request: HttpRequest):
    if request.method == 'POST':
        params = request.POST.values()
        response = HttpResponseRedirect(reverse('doctor_list'))
        specializations = json.dumps(params)
        response.set_cookie('selected_specializations', specializations, max_age=3600)
        return response

def select_languages(request: HttpRequest):
    if request.method == 'POST':
        params = request.POST.values()
        response = HttpResponseRedirect(reverse('doctor_list'))
        languages = json.dumps(params)
        response.set_cookie('selected_languages', languages, max_age=3600)
        return response

def select_gender(request: HttpRequest):
    if request.method == 'POST':
        params = request.POST.values()
        response = HttpResponseRedirect(reverse('doctor_list'))
        languages = json.dumps(params)
        response.set_cookie('selected_genders', languages, max_age=3600)
        return response