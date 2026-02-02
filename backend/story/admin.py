from django.contrib import admin
from .models import Stories, Chapters, Paragraphs

admin.site.register(Paragraphs)
admin.site.register(Stories)
admin.site.register(Chapters)
