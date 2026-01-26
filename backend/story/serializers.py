from backend import story
from rest_framework import serializers #type: ignore
from html import unescape
from django.db import transaction
from django.db.models import Max
from .models import Stories, Chapters, Paragraphs
from .services.services_chapter_add import split_paragraphs as service_split_paragraphs
from .services.services_chapter_add import create_chapter_atomic as service_create_chapter_atomic

class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ["id", "title", "description"]

class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapters
        fields = ["id", "title", "number", "dictionary_completed"]



class ChapterAddSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()

    def validate_title(self, value):
        value = unescape(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_content(self, value):
        value = unescape(value).strip()
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
        return service_create_chapter_atomic(
            story=story,
            title=title,
            paragraph_list=paragraph_list,
        )
