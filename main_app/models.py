from django.db import models
from django.urls import reverse
from phone_field import PhoneField 


class Contractor(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.FloatField(default=0)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('contractors_detail', kwargs={'pk': self.id})

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
  review = models.TextField(max_length=200, blank=True)
  contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)

  def __str__(self):
        return f'{self.contractor} - {self.rating}'

  class Meta:
    ordering = ['-date']


class User(models.Model):
  name = models.CharField(max_length=100)
  phone = PhoneField(blank=True, help_text='Contact phone number')
  email = models.EmailField(max_length=150)
  location = models.CharField(max_length=150)
  rating = models.FloatField(default=0)
  review = models.ForeignKey(Review, default=None, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('user_detail', kwargs={'pk': self.id})


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