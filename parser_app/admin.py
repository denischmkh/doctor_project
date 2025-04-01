from django.contrib import admin
from .models import (
    Doctor, Clinic, Language, Hospital, Specialisation, Education, WorkExperience,
    Apprenticeship, Publication, Research, Award, Competence, Membership
)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'city', 'gender')
    search_fields = ('name', 'phone', 'email', 'city')
    list_filter = ('city', 'gender')
    list_per_page = 50
    ordering = ['id']

    # ✅ Используем autocomplete для ManyToMany
    autocomplete_fields = ['clinic', 'languages', 'hospitals', 'specialisations',
                           'educations', 'work_experience', 'apprenticeships',
                           'publications', 'researches', 'awards', 'competences', 'memberships']

    # ❌ Убираем filter_horizontal (он замедляет админку на больших данных)
    filter_horizontal = []

    # ❌ Убираем поля, которые не нужны в форме редактирования
    exclude = ['media_urls']

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("title", "location")
    search_fields = ("title", "location")

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Specialisation)
class SpecialisationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("info", "year")
    search_fields = ("info", "year")

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("info", "year")
    search_fields = ("info", "year")

@admin.register(Apprenticeship)
class ApprenticeshipAdmin(admin.ModelAdmin):
    list_display = ("info", "year")
    search_fields = ("info", "year")

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "year")
    search_fields = ("title", "year")

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("title", "year")
    search_fields = ("title", "year")

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    search_fields = ("name", "year")

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

