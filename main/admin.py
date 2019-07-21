from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import handles
# Register your models here.


@admin.register(handles)
class ViewAdmin(ImportExportModelAdmin):
   pass