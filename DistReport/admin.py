from django.contrib import admin
from .models import DistReport, Task, Response
# Register your models here.

admin.site.register(DistReport)
admin.site.register(Task)
admin.site.register(Response)