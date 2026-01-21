from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import Storys
from .serializers import StorysSerializer

class StorysListView(ListAPIView):
    queryset = Storys.objects.all().order_by("id")
    serializer_class = StorysSerializer

