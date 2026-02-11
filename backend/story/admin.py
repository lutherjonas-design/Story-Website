from django.contrib import admin
from .models import Story, Chapter, Paragraph

admin.site.register(Paragraph)
admin.site.register(Story)
admin.site.register(Chapter)
