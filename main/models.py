from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subjects")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

"""class Note(models.Model):
    title = models.CharField(max_length=200)
    filename = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="notes")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title"""


from django.db import models
from django.utils import timezone

class Note(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    file_size = models.BigIntegerField(null=True, blank=True)# This handles path, name, size
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name="notes")
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


