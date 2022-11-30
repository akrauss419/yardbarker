import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Job, Member, Review, Contractor, JobPhoto, MemberPhoto, ContractorPhoto
from .forms import ReviewForm, JobCreateForm, MemberCreateForm
from django.contrib.auth.models import User


def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


@login_required
def member_detail(request):
  curr_member = Member.objects.get(user=request.user)
  job_list = Job.objects.filter(member=curr_member).order_by('-isDone')
  completed_list = job_list.filter(isDone='1')
  not_complete_list = job_list.filter(isDone='2')
  
  return render(request, 'member_detail.html', {
    'member': curr_member,
    'job_list': job_list,
    'completed_list': completed_list,
    'not_complete_list': not_complete_list,
  })


@login_required
def jobs_index(request):
  jobs = Job.objects.filter(isDone='2')
  return render(request, 'jobs/index.html', {
    'jobs': jobs
  })


@login_required
def assoc_contractor(request, job_id, contractor_id):
  Job.objects.get(id=job_id).contractors.add(contractor_id)
  return redirect('detail', job_id = job_id)


@login_required
def jobs_detail(request, job_id):
  job = Job.objects.get(id=job_id)
  id_list = job.contractors.all().values_list('id')
  contractors_available = Contractor.objects.exclude(id__in=id_list)
  return render(request, 'jobs/detail.html', {
    'job': job,
    'contractors': contractors_available
  })


class JobUpdate(LoginRequiredMixin, UpdateView):
  model = Job
  fields = ['name', 'task', 'location', 'reward', 'description', 'isDone']


class JobDelete(LoginRequiredMixin, DeleteView):
  model = Job
  success_url = '/jobs'


class ContractorList(LoginRequiredMixin, ListView):
  model = Contractor


class ContractorDetail(LoginRequiredMixin, DetailView):
  model = Contractor


class ContractorCreate(LoginRequiredMixin, CreateView):
  model = Contractor
  fields = ['name', 'phone', 'email', 'location']


class ContractorUpdate(LoginRequiredMixin, UpdateView):
  model = Contractor
  fields = ['phone', 'email', 'location']


class ContractorDelete(LoginRequiredMixin, DeleteView):
  model = Contractor
  success_url = '/contractors'


def jobs_create(request):
  member = Member.objects.get(user=request.user)
  error_message = ''
  job_create_form = JobCreateForm()
  if request.method == 'POST':
    form = JobCreateForm(request.POST)
    if form.is_valid():
      new_job = form.save(commit=False)
      new_job.isDone = '2'
      new_job.member = member
      new_job.save()
      return redirect('detail', job_id=new_job.id)
    else:
      error_message = 'You are not a member or this is an invalid form'
  return render(request, 'jobs/create.html', {
    'member': member,
    'job_create_form': job_create_form,
    'error_message': error_message
  })


def member_create(request):
  error_message = ''
  member_create_form = MemberCreateForm()
  if request.method == 'POST':
    form = MemberCreateForm(request.POST)
    if form.is_valid():
      new_member = form.save(commit=False)
      new_member.user = request.user
      new_member.save()
      return redirect('member_detail')
    else:
      error_message = 'You are not a member or this is an invalid form'
  return render(request, 'member_create.html', {
    'member_create_form': member_create_form,
    'error_message': error_message
  })


class MemberUpdate(UpdateView):
  model = Member
  fields = ['name', 'phone', 'email', 'location']


@login_required
def add_job_photo(request, job_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + \
      photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      JobPhoto.objects.create(url=url, job_id=job_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
    return redirect('detail', job_id=job_id)


@login_required
def add_contractor_photo(request, contractor_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      ContractorPhoto.objects.create(url=url, contractor_id=contractor_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
    return redirect('contractors_detail', contractor_id=contractor_id)


@login_required
def add_review(request, contractor_id):
  form = ReviewForm(request.POST)
  curr_contractor = Contractor.objects.get(id=contractor_id)
  print(request.user)
  curr_member = Member.objects.get(user=request.user)
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.contractor = curr_contractor
    new_review.member = curr_member
    new_review.save()
    print(new_review)
  return redirect('contractors_detail', contractor_id=contractor_id)


def contractors_detail(request, contractor_id):
  contractor = Contractor.objects.get(id=contractor_id)
  contractor_rev = Review.objects.filter(contractor=contractor_id)
  sum = 0
  for review in contractor_rev:
    print(f"rating: {float(review.rating)}")
    sum += float(review.rating)
  if sum == 0:
    average = 0
  else:
    average = round(sum / len(contractor_rev), 1)
  form = ReviewForm()
  return render(request, 'main_app/contractor_detail.html', {
    'contractor': contractor,
    'review_form': form,
    'average': average,
  })


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('members_create')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)