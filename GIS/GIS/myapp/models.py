from django.db import models


class HardwareData(models.Model):
    name = models.CharField(max_length=100, db_column='Name')
    location = models.CharField(max_length=255, db_column='Location')
    longitude = models.FloatField(db_column='Longitude')
    latitude = models.FloatField(db_column='Latitude')
    url = models.FileField(db_column='URL', null=True, blank=True)
    region = models.TextField(db_column='region', null=True, blank=True)
    status = models.BooleanField(db_column='Status', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mstr_camera'


class GISNotification(models.Model):
    id = models.AutoField(primary_key=True)
    camera_ip = models.CharField(max_length=50, db_column="CameraIP")
    name = models.CharField(max_length=255, db_column="Name")
    region = models.CharField(max_length=255, db_column="Region")
    location = models.CharField(max_length=255, db_column="Location")
    created_date = models.DateTimeField(db_column="Created_Date")

    popup_shown = models.BooleanField(db_column="PopUp_Shown", default=False)

    class Meta:
        managed = False
        db_table = "GIS_Notification"

    def __str__(self):
        return f"{self.camera_ip} - {self.name} ({self.region})"







