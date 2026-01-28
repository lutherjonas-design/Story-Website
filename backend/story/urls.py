from django.urls import path
from .views import StoriesListView, ChaptersListView, ChapterAddView, ShowChapterView

urlpatterns = [
    path("stories/", StoriesListView.as_view(), name="stories-list"),
    path("stories/<int:story_id>/chapters/", ChaptersListView.as_view(), name="chapters-list"),
    path("stories/<int:story_id>/chapters/add/", ChapterAddView.as_view(), name="chapter-add"),
    path("stories/<int:story_id>/<int:chapter_order>/", ShowChapterView.as_view(), name="chapter-view"),
]
