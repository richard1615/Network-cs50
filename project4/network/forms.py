from django import forms
from django.forms import ModelForm

from .models import posts

class postForm(ModelForm):
    class Meta:
        model = posts
        fields = ['content']