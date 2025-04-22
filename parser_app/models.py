import re

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import IntegerField, CharField, TextField, Model, ForeignKey, URLField, JSONField, ManyToManyField
from django.utils.text import slugify
from unidecode import unidecode


class Language(models.Model):
    name = TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unknown Language"


class Hospital(models.Model):
    name = TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Hospital"


class Specialisation(models.Model):
    name = models.TextField(blank=True, unique=False)
    slug = models.SlugField(max_length=10000, unique=False, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Specialisation"


class Education(models.Model):
    info = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})" if self.info else "Unknown Education"


class WorkExperience(models.Model):
    info = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})" if self.info else "No Work Experience"


class Apprenticeship(models.Model):
    info = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})" if self.info else "No Apprenticeship"


class Publication(models.Model):
    title = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year if self.year else 'N/A'})" if self.title else "No Publication"


class Research(models.Model):
    title = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year if self.year else 'N/A'})" if self.title else "No Research"


class Award(models.Model):
    name = TextField(null=True, blank=True)
    year = CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.year if self.year else 'N/A'})" if self.name else "No Award"


class Competence(models.Model):
    name = TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "No Competence"


class Membership(models.Model):
    name = TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "No Membership"


class Clinic(models.Model):
    title = CharField(max_length=255, null=True, blank=True)
    location = CharField(max_length=255, null=True, blank=True)
    image = URLField(null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Unnamed Clinic"


class Doctor(models.Model):

    name = models.CharField(max_length=1000,null=True)
    clinic = models.ManyToManyField(Clinic, blank=True)
    description = models.TextField(null=True)
    profile_url = models.URLField(null=True)
    phone = models.CharField(max_length=1000,null=True)
    email = models.CharField(max_length=1000,null=True)
    vcard_url = models.URLField(max_length=1000,null=True)
    cv_url = models.URLField(max_length=1000,null=True)
    photo_url = models.URLField(max_length=1000,null=True)


    gender = models.CharField(null=True)
    city = models.CharField(null=True)


    address = models.CharField(null=True)
    fax = models.CharField(max_length=10000,null=True)
    instagram = models.URLField(max_length=10000,null=True)
    facebook = models.URLField(max_length=10000,null=True)
    twitter = models.URLField(max_length=10000,null=True)
    linkedin = models.URLField(max_length=10000,null=True)
    youtube = models.URLField(max_length=10000,null=True)

    languages = models.ManyToManyField(Language, blank=True)
    hospitals = models.ManyToManyField(Hospital, blank=True)
    specialisations = models.ManyToManyField(Specialisation, blank=True)
    educations = models.ManyToManyField(Education, blank=True)
    work_experience = models.ManyToManyField(WorkExperience, blank=True)
    apprenticeships = models.ManyToManyField(Apprenticeship, blank=True)
    publications = models.ManyToManyField(Publication, blank=True)
    researches = models.ManyToManyField(Research, blank=True)
    awards = models.ManyToManyField(Award, blank=True)
    competences = models.ManyToManyField(Competence, blank=True)
    memberships = models.ManyToManyField(Membership, blank=True)

    site_url = models.URLField(max_length=10000, null=True)
    media_urls = models.JSONField(null=True, blank=True)

    source = models.CharField(null=True, max_length=10000)
    postcode = models.CharField(null=True, max_length=5000)

    def __str__(self):
        return self.name if self.name else "Unnamed Doctor"