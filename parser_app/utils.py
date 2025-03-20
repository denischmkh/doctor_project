def get_specialists_count(specialization_name: str, doctors) -> int:
    specialization_count = 0
    for doctor in doctors:
        if doctor.specialisations.filter(name=specialization_name).exists():
            specialization_count += 1
    return specialization_count
