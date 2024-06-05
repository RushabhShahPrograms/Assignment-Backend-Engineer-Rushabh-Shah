from django.db import models

# Create your models here.


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')


class ColorResult(models.Model):
    strip_id = models.AutoField(primary_key=True)
    results = models.JSONField()

    def __str__(self):
        return str(self.strip_id)