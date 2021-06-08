from django.contrib import admin
from .models import User, Post, Fallower

# Register your models here.

admin.site.register(Post)
admin.site.register(Fallower)
admin.site.register(User)
