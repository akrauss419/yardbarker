from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phone_field import PhoneField
from django import forms


class Contractor(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.FloatField(default=0)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('contractors_detail', kwargs={'contractor_id': self.id})


class Member(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.FloatField(default=0)
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('user_detail', kwargs={'pk': self.id})


class Review(models.Model):
  RATING_CHOICES = (
    ('1', '⭐️'),
    ('2', '⭐️⭐️'),
    ('3', '⭐️⭐️⭐️'),
    ('4', '⭐️⭐️⭐️⭐️'),
    ('5', '⭐️⭐️⭐️⭐️⭐️')
  )

  date = models.DateField(auto_now_add=True)
  rating = models.CharField(max_length=1, choices=RATING_CHOICES, blank=True)
  content = models.TextField(max_length=500, blank=True)
  contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
  member = models.ForeignKey(Member, default=None, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.contractor} - {self.rating}'

  class Meta:
    ordering = ['-date']


class Job(models.Model):
  DONE_OR_NOT = (
    ('1', 'Done'),
    ('2', 'Not Done')
  )

  name = models.CharField(max_length=100)
  task = models.CharField(max_length=150)
  location = models.CharField(max_length=100)
  reward = models.IntegerField()
  description = models.TextField(max_length=250)
  isDone = models.CharField(choices=DONE_OR_NOT, default='2', max_length=1)
  member = models.ForeignKey(Member, default=None, on_delete=models.CASCADE)
  contractors = models.ManyToManyField(Contractor)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'job_id': self.id})


class JobPhoto(models.Model):
  url = models.CharField(max_length=200)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for job_id: {self.job_id} @{self.url}"


class MemberPhoto(models.Model):
  url = models.CharField(max_length=200)
  member = models.ForeignKey(Member, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for Member_id: {self.member_id} @{self.url}"


class ContractorPhoto(models.Model):
  url = models.CharField(max_length=200)
  contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for Contractor_id: {self.contractor_id} @{self.url}"