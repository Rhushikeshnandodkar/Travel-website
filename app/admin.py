from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
# Register your models here.

class customer_list(resources.ModelResource):
    class Meta:
        model = PlaceMode
        fields = ('id', 'Name', 'City', 'Zone', 'Type', 'State', 'Description', 'Year' ,'Time_needed', 'Google_rating', 'Significance', 'Best_time_to_visit', 'Fees')
class UserAdmin(ImportExportModelAdmin):
    resource_class = customer_list
admin.site.register(PlaceMode, UserAdmin)

class crowd_data(resources.ModelResource):
    location = fields.Field(
        column_name='location',
        attribute='location',
        widget=ForeignKeyWidget(PlaceMode, 'id')  # Assuming you want to match by the name of the PlaceModel
    )
    class Meta:
        model = CrowdModel
        fields = ('location', 'month_name', 'crowd_count')
        import_id_fields = ('location', 'month_name')  # Ensure we use location and month for imports
        skip_unchanged = True  # Skip unchanged records
        report_skipped = True  # Report skipped records
        update_existing = True 
class CrowdAdmin(ImportExportModelAdmin):
    resource_class = crowd_data
admin.site.register(CrowdModel, CrowdAdmin)
admin.site.register(ReviewModel)