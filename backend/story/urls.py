from django.urls import path
from .views import StorysListView

urlpatterns = [
    path("stories/", StorysListView.as_view(), name="stories-list"),
]
