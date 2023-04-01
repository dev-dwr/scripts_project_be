from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Industry(models.TextChoices):
    Finance = 'Finance'
    IT = 'Information Technology'
    Banking = 'Banking'
    Education = 'Education'
    Telecommunication = 'Telecommunication'


class JobType(models.TextChoices):
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Internship = 'Internship'


class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Years'
    TWO_YEAR = '2 Years'


def return_expiration_date_time():
    return datetime.now() + timedelta(days=5)


class Offer(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    experience = models.CharField(max_length=22, choices=Experience.choices, default=Experience.NO_EXPERIENCE)
    month_salary = models.IntegerField(default=1, validators=[MinValueValidator(500), MaxValueValidator(20_000)])
    positions = models.IntegerField(default=1)
    company = models.CharField(max_length=50, null=True)
    expiration_date = models.DateTimeField(default=return_expiration_date_time)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=70, null=True)
    job_type = models.CharField(max_length=10, choices=JobType.choices, default=JobType.Internship)
    industry = models.CharField(max_length=30, choices=Industry.choices, default=Industry.Finance)


class Candidate(models.Model):
    cv = models.CharField(max_length=150)
    applied_at = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
