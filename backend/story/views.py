from rest_framework.generics import ListAPIView, CreateAPIView #type: ignore
from rest_framework.views import APIView #type: ignore
from rest_framework.response import Response #type: ignore
from .models import Stories, Chapters, Paragraphs, UniqueWordsInParagraphs, Dictionary, WordsToAdd
from .serializers import StoriesSerializer,ChapterListSerializer,ChapterAddSerializer, ShowChapterSerializer, WordsToAddViewSerializer
from .services.reformatting_text import (
    reformat_text_output as service_reformat_output,
    get_words as service_get_words
)

class StoriesListView(ListAPIView):
    queryset = Stories.objects.all().order_by("id")
    serializer_class = StoriesSerializer

class ChaptersListView(ListAPIView):
    serializer_class = ChapterListSerializer

    def get_queryset(self):
        story_id = self.kwargs['story_id']
        return Chapters.objects.filter(story_id=story_id).order_by("order")

class ShowChapterView(APIView):
    serializer_class = ShowChapterSerializer
    def get(self,rquest,story_id:int,chapter_order:int,*args,**kwargs):
        chapter = Chapters.objects.filter(story_id=story_id, order=chapter_order).only("id", "title", "story_id").first()
        print(chapter)
        if not chapter:
            payload = {
                "chapter_id": None,
                "title": [],
                "paragraphs": [],
                "dictionary": dict({}),
            }
            return Response(ShowChapterSerializer(payload).data)
        unique_words_title = service_get_words(chapter.title)
        #paragraphs = chapter.paragraphs_set.all().order_by("number").only("id", "number", "content")
        db_paragraphs = Paragraphs.objects.filter(chapter_id=chapter.id).only("id", "number", "content").order_by("number")
        paragraph_formatted = [{"id":id,"n":n,"t":service_reformat_output(p)} for id,n,p in db_paragraphs.values_list("id","number","content")]
        paragraph_ids = db_paragraphs.values_list("id", flat=True)
        unique_paragraph_words = set(UniqueWordsInParagraphs.objects.filter(paragraph_id__in=paragraph_ids).values_list("word", flat=True).distinct())
        unique_words = unique_paragraph_words | set(unique_words_title)
        normalized_unique_words = {word.lower() for word in unique_words}
        db_dictionary = Dictionary.objects.filter(word__in=normalized_unique_words).values_list("word","syllable_breaks")
        dictionary_words = {w:breaks for (w, breaks) in db_dictionary}
        payload = { # still need to add the words of tittle to the dictionary querryset
            "chapter_id": chapter.id,
            "title": service_reformat_output(chapter.title),
            "paragraphs": paragraph_formatted,
            "dictionary": dictionary_words,
        }
        return Response(ShowChapterSerializer(payload).data)

class ChapterAddView(CreateAPIView):
    serializer_class = ChapterAddSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["story_id"] = self.kwargs["story_id"]  # inject the URL parameter
        return ctx
    
class WordsToAddView(ListAPIView):
    serializer_class = WordsToAddViewSerializer

    def get_queryset(self):
        params = self.request.query_params
        if 'limit' in params:
            if params['limit'].isdigit():
                limit = int(params['limit'])
                return WordsToAdd.objects.all().order_by("-frequency")[:limit].values_list()
        return WordsToAdd.objects.all().order_by("-frequency")[:10].values_list()