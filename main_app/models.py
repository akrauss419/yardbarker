from django.db import models
from django.urls import reverse
from phone_field import PhoneField 

# Create your models here.

class Review(models.Model):
  content = models.CharField(max_length=150)
  date = models.DateField('Review date')
  rating = models.IntegerField()

  def __str__(self):
    return f"Reviewed on {self.date}"


class User(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.IntegerField()
  review = models.ForeignKey(Review, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('user_detail', kwargs={'pk': self.id})


class Contractor(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.IntegerField()
  review = models.ForeignKey(Review, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('contractors_detail', kwargs={'pk': self.id})


class Job(models.Model):
  name = models.CharField(max_length=100)
  task = models.CharField(max_length=150)
  location = models.CharField(max_length=100)
  # aka pricing
  reward = models.IntegerField()
  description = models.TextField(max_length=250)
  isDone = models.BooleanField(default=False)
  # M:M users
  posters = models.CharField(max_length=100)
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


class UserPhoto(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for User_id: {self.user_id} @{self.url}"

class ContractorPhoto(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for Contractor_id: {self.contractor_id} @{self.url}"
