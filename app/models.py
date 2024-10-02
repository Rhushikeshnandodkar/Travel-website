from django.db import models

# Create your models here.
class PlaceMode(models.Model):
    place_id = models.IntegerField(null=True, blank=True)
    Name = models.CharField(max_length=200, null=True, blank=True)
    City = models.CharField(max_length=200, blank=True, null=True)
    Zone = models.CharField(max_length=200, blank=True, null=True)
    Type = models.CharField(max_length=200, blank=True, null=True)
    State = models.CharField(max_length=200, null=True, blank=True)
    Description = models.CharField(max_length=200, null=True, blank=True)
    Year = models.CharField(max_length=200, null=True, blank=True)
    Time_needed = models.CharField(max_length=200, null=True, blank=True)
    Google_rating = models.CharField(max_length=200, null=True, blank=True)
    Significance = models.CharField(max_length=200, null=True, blank=True)
    Best_time_to_visit = models.CharField(max_length=200, null=True, blank=True)
    Fees = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Name




   
