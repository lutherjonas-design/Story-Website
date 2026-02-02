from django.contrib import admin
from .models import Dictionary, WordsToAdd

# Register your models here.
admin.site.register(Dictionary)
admin.site.register(WordsToAdd)