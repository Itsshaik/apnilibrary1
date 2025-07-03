from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Class, Subject, Note

admin.site.register(User)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Note)