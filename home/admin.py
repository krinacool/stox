from django.contrib import admin
from home.models import *

# Register your models here.
@admin.register(News)
class News(admin.ModelAdmin):
    list_display = ('title', 'datetime')

@admin.register(CA)
class CA(admin.ModelAdmin):
    list_display = ('title', 'datetime')