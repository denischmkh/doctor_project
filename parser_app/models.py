from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import IntegerField, CharField, TextField, Model, ForeignKey, URLField, JSONField, ManyToManyField

class Language(models.Model):
    name = TextField(null=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = TextField(null=True)

    def __str__(self):
        return self.name

class Specialisation(models.Model):
    name = TextField(null=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    info = TextField()
    year = CharField(null=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})"

class WorkExperience(models.Model):
    info = TextField()
    year = CharField(null=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})"

class Apprenticeship(models.Model):
    info = TextField()
    year = CharField(null=True)

    def __str__(self):
        return f"{self.info} ({self.year if self.year else 'N/A'})"

class Publication(models.Model):
    title = TextField(null=True)
    year = CharField(null=True)

    def __str__(self):
        return f"{self.title} ({self.year if self.year else 'N/A'})"

class Research(models.Model):
    title = TextField(null=True)
    year = CharField(null=True)

    def __str__(self):
        return f"{self.title} ({self.year if self.year else 'N/A'})"

class Award(models.Model):
    name = TextField(null=True)
    year = CharField(null=True)

    def __str__(self):
        return f"{self.name} ({self.year if self.year else 'N/A'})"

class Competence(models.Model):
    name = TextField(null=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    name = TextField(null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.TextField(null=True)
    clinic = models.TextField(null=True)
    description = models.TextField(null=True)
    profile_url = models.URLField(null=True)
    phone = models.TextField(null=True)
    email = models.TextField(null=True)
    vcard_url = models.URLField(null=True)
    cv_url = models.URLField(null=True)
    photo_url = models.URLField(null=True)

    address = models.TextField(null=True)
    fax = models.TextField(null=True)
    instagram = models.TextField(null=True)
    facebook = models.TextField(null=True)
    twitter = models.TextField(null=True)
    linkedin = models.TextField(null=True)
    youtube = models.TextField(null=True)

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

    site_url = models.TextField(null=True)
    media_urls = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
