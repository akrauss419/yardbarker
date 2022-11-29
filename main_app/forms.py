from django.forms import ModelForm
from django import forms
from .models import Review, Job, Member


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']


class JobCreateForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = ['name', 'task', 'location', 'reward', 'description']


class MemberCreateForm(forms.ModelForm):
  class Meta:
    model = Member
    fields = ['name', 'phone', 'email', 'location']