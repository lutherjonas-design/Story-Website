from rest_framework import serializers #type: ignore
from .models import Stories, Chapters

from dictionary.models import Dictionary, WordsToAdd

from .helper.reformatting_text import(
    split_paragraphs as service_split_paragraphs,
    sanitize_text as service_sanitize_text
)
from .helper.chapter_add import create_words_statistsics as service_create_words_statistics  
from .helper.database import create_chapter_atomic as service_create_chapter_atomic

class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ["id", "title", "description"]


class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = ["id", "title", "order", "dictionary_completed"]


class ShowChapterSerializer(serializers.Serializer):
    chapter_id = serializers.IntegerField(allow_null=True)
    title = serializers.ListField(
        child=serializers.JSONField(),
        allow_empty=True
    )
    paragraphs = serializers.ListField(
        child=serializers.JSONField(),
        allow_empty=True
    )
    dictionary = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField(min_value=0)),
        allow_empty=True,
    )


class ChapterAddSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(write_only=True)

    def validate_title(self, value):
        value = service_sanitize_text(value)
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_content(self, value):
        value = service_sanitize_text(value)
        if not value:
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def create(self, validated_data):
        story_id = self.context["story_id"]
        title = validated_data["title"]
        content = validated_data["content"]
        
        try: # Validate story existence
            story = Stories.objects.get(id=story_id)
        except Stories.DoesNotExist:
            raise serializers.ValidationError("Story does not exist")

        paragraph_list = service_split_paragraphs(content)
        words_to_add,chapter_word_set = service_create_words_statistics(paragraph_list=paragraph_list)
        return service_create_chapter_atomic(
            story=story,
            title=title,
            paragraph_list=paragraph_list,
            words_to_add=words_to_add,
            chapter_word_set=chapter_word_set,
        )


class CanditatesToDictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    #syllables = serializers.ArrayField()
    def validate(self, data):
        word_id = data["id"]
        try:
            word = WordsToAdd.objects.get(id=word_id).only("word").first()
        except WordsToAdd.DoesNotExist:
            raise serializers.ValidationError("Word not in WordsToAdd")
        data["word"] = word
    pass


class WordsToAddViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsToAdd
        fields = ["id", "word", "frequency"]