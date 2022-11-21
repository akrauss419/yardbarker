from django.contrib import admin
from .models import Job, User, Review, Contractor, JobPhoto, UserPhoto, ContractorPhoto

# Register your models here.
admin.site.register(Job)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Contractor)
admin.site.register(JobPhoto)
admin.site.register(UserPhoto)
admin.site.register(ContractorPhoto)