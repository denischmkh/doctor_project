from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Doctor, Specialisation
from .utils import get_specialists_count


def doctor_list(request, page=1):

    unique_specializations = set()
    all_specializations = Specialisation.objects.all()
    for specialization in all_specializations:
        unique_specializations.add(specialization.name)
    print(unique_specializations)
    print(len(unique_specializations))

    per_page = 7
    end = page * per_page
    start = end - per_page
    if start == 0:
        previous_page = None
    else:
        previous_page = page - 1
    doctors = Doctor.objects.all()[start:end]
    if len(doctors) < per_page - 1:
        next_page = None
    else:
        next_page = page + 1

    doctors_count = len(Doctor.objects.all())



    urology_count = get_specialists_count(doctors=doctors, specialization_name='Urology')
    psychiatry_count = get_specialists_count(doctors=doctors, specialization_name='Psychotherapy')
    cardiology_count = get_specialists_count(doctors=doctors, specialization_name='Cardiology')
    paediatrics_count = get_specialists_count(doctors=doctors, specialization_name='Paediatrics')
    neurology_count = get_specialists_count(doctors=doctors, specialization_name='Neurology')
    pulmonology_count = get_specialists_count(doctors=doctors, specialization_name='Pulmonology')
    orthopedics_count = get_specialists_count(doctors=doctors, specialization_name='Orthopedics')
    endocrinology_count = get_specialists_count(doctors=doctors, specialization_name='Endocrinology')



    return render(request, 'search-2.html', {'doctors': doctors,
                                             'doctors_count': doctors_count,
                                             'urology_count': urology_count,
                                             'psychiatry_count': psychiatry_count,
                                             'cardiology_count': cardiology_count,
                                             'paediatrics_count': paediatrics_count,
                                             'neurology_count': neurology_count,
                                             'pulmonology_count': pulmonology_count,
                                             'orthopedics_count': orthopedics_count,
                                             'endocrinology_count': endocrinology_count,
                                             'previous_page': previous_page,
                                             'next_page': next_page,
                                             'page': page})


def doctor_profile(request, id: int):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'doctor-profile-2.html', {'doctor': doctor})