from django.contrib import admin
from .models import Job, Member, Review, Contractor, JobPhoto, MemberPhoto, ContractorPhoto

# Register your models here.
admin.site.register(Job)
admin.site.register(Member)
admin.site.register(Review)
admin.site.register(Contractor)
admin.site.register(JobPhoto)
admin.site.register(MemberPhoto)
admin.site.register(ContractorPhoto)