from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Doctor
from .utils import get_specialists_count


def doctor_list(request, page=1):
    doctors = Doctor.objects.all()[:100]
    for doctor in doctors:
        specializations = doctor.specialisations.all()
        for specialization in specializations:
            if specialization.name.startswith('{') and specialization.name.endswith('}'):
                specialization.name = specialization.name[1:-1].split(', ')[0]
                specialization.save()
    paginator = Paginator(object_list=doctors, per_page=7)
    doctors_paginator = paginator.page(page)


    urology_count = get_specialists_count(doctors=doctors, specialization_name='Urology')
    psychiatry_count = get_specialists_count(doctors=doctors, specialization_name='Psychotherapy')
    cardiology_count = get_specialists_count(doctors=doctors, specialization_name='Cardiology')
    paediatrics_count = get_specialists_count(doctors=doctors, specialization_name='Paediatrics')
    neurology_count = get_specialists_count(doctors=doctors, specialization_name='Neurology')
    pulmonology_count = get_specialists_count(doctors=doctors, specialization_name='Pulmonology')
    orthopedics_count = get_specialists_count(doctors=doctors, specialization_name='Orthopedics')
    endocrinology_count = get_specialists_count(doctors=doctors, specialization_name='Endocrinology')



    return render(request, 'search-2.html', {'doctors': doctors_paginator,
                                             'doctors_count': len(doctors),
                                             'urology_count': urology_count,
                                             'psychiatry_count': psychiatry_count,
                                             'cardiology_count': cardiology_count,
                                             'paediatrics_count': paediatrics_count,
                                             'neurology_count': neurology_count,
                                             'pulmonology_count': pulmonology_count,
                                             'orthopedics_count': orthopedics_count,
                                             'endocrinology_count': endocrinology_count})


def doctor_profile(request, id: int):
    doctor = get_object_or_404(Doctor, id=id)
    specializations = doctor.specialisations.all()
    for specialization in specializations:
        if specialization.name.startswith('{') and specialization.name.endswith('}'):
            specialization.name = specialization.name[1:-1].split(', ')[0]
            specialization.save()
    return render(request, 'doctor-profile-2.html', {'doctor': doctor})