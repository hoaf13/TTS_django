from django.db import models
from django.contrib import admin
# Create your models here.

class RecorderModel(models.Model):
    GENDERS = ((2, 'New Voice'),(11, 'Old Voice'))

    gender = models.IntegerField(default=0, choices=GENDERS)
    content = models.TextField(max_length=2000)
    audio = models.FileField(null=True,upload_to='audios/')

class RecorderModelAdmin(admin.ModelAdmin):
    list_display =  ['id','content','gender','audio']
    