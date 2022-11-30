from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('members/', views.member_detail, name='member_detail'),
  path('members/create/', views.member_create, name='members_create'),
  path('jobs/', views.jobs_index, name='index'),
  path('jobs/<int:job_id>/', views.jobs_detail, name='detail'),
  path('jobs/create/', views.jobs_create, name='jobs_create'),
  path('jobs/<int:pk>/update', views.JobUpdate.as_view(), name='jobs_update'),
  path('jobs/<int:pk>/delete', views.JobDelete.as_view(), name='jobs_delete'),
  path('jobs/<int:job_id>/add_job_photo', views.add_job_photo, name='add_job_photo'),
  path('jobs/<int:job_id>/assoc_contractor/<int:contractor_id>/', views.assoc_contractor, name='assoc_contractor'),
  path('contractors/', views.ContractorList.as_view(), name='contractors_index'),
  path('contractors/<int:contractor_id>/', views.contractors_detail, name='contractors_detail'),
  path('contractors/create/', views.ContractorCreate.as_view(), name='contractors_create'),
  path('contractors/<int:pk>/update/', views.ContractorUpdate.as_view(), name='contractors_update'),
  path('contractors/<int:pk>/delete/', views.ContractorDelete.as_view(), name='contractors_delete'),
  path('contractors/<int:contractor_id>/add_contractor_photo', views.add_contractor_photo, name='add_contractor_photo'),
  path('contractors/<int:contractor_id>/add_review/', views.add_review, name='add_review'),
  path('accounts/signup/', views.signup, name='signup'),
]