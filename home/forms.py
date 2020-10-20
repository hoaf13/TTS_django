from django import forms
from .models import *


class RecorderForm(forms.ModelForm):

    class Meta:
        model = RecorderModel
        fields = ['gender','content']