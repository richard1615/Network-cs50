from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass

class posts(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = RichTextField(max_length=500)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField()

