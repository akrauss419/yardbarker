import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Job, User, Review, Contractor, JobPhoto, UserPhoto, ContractorPhoto

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def jobs_index(request):
  jobs = Job.objects.filter(posters=request.user)
  return render(request, 'jobs/index.html', {
    'jobs': jobs
  })

@login_required
def jobs_detail(request, job_id):
  job = Job.objects.get(id=job_id)
  return render(request, 'jobs/detail.html', {
    'job': job
  })

class JobCreate(LoginRequiredMixin, CreateView):
  model = Job
  fields = ['name', 'task', 'location', 'reward', 'description', 'posters']

class JobUpdate(LoginRequiredMixin, UpdateView):
  model = Job
  fields = ['name', 'task', 'location', 'reward', 'description']

class JobDelete(LoginRequiredMixin, DeleteView):
  model = Job
  success_url = '/jobs'


@login_required
def add_job_photo(request, job_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      JobPhoto.objects.create(url=url, job_id=job_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
    return redirect('detail', job_id=job_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)