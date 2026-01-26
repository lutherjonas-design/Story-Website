from rest_framework.generics import ListAPIView, CreateAPIView #type: ignore
from .models import Stories, Chapters
from .serializers import StoriesSerializer,ChapterListSerializer,ChapterAddSerializer#, ShowChapterSerializer

class StoriesListView(ListAPIView):
    queryset = Stories.objects.all().order_by("id")
    serializer_class = StoriesSerializer

class ChaptersListView(ListAPIView):
    serializer_class = ChapterListSerializer
    
    def get_queryset(self):
        story_id = self.kwargs['story_id']
        return Chapters.objects.filter(story_id=story_id).order_by("number")
    
#class ShowChapterView(CreateAPIView):
#    serializer_class = ShowChapterSerializer
#    def get_serializer_context(self):
#        story_id = self.kwargs['story_id']
#        chapter_number = self.kwargs['chapter_number']


class ChapterAddView(CreateAPIView):
    serializer_class = ChapterAddSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["story_id"] = self.kwargs["story_id"]  # inject the URL parameter
        return ctx


