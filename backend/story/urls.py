from django.urls import path
from .views import StoriesListView, ChaptersListView, ChapterAddView, ShowChapterView 

urlpatterns = [ # /api/stories/
    path("", StoriesListView.as_view(), name="story-list"),
    path("<int:story_id>/chapters/", ChaptersListView.as_view(), name="chapters-list"),
    path("<int:story_id>/chapters/add/", ChapterAddView.as_view(), name="chapter-add"),
    path("<int:story_id>/<int:chapter_order>/", ShowChapterView.as_view(), name="chapter-view"),
]
