from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class customer_list(resources.ModelResource):
    class Meta:
        model = PlaceMode
        fields = ('id', 'Name', 'City', 'Zone', 'Type', 'State', 'Description', 'Year' ,'Time_needed', 'Google_rating', 'Significance', 'Best_time_to_visit', 'Fees')
class UserAdmin(ImportExportModelAdmin):
    resource_class = customer_list
admin.site.register(PlaceMode, UserAdmin)