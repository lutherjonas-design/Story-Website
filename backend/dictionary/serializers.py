from rest_framework import serializers #type: ignore
from rest_framework.exceptions import NotFound, ValidationError #type: ignore
from .models import WordsToAdd



class CandidatesToDictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    syllables = serializers.ListField(
        child = serializers.CharField(min_length=1),
        allow_empty = False
    )

    def validate(self, attrs):
        word_id = attrs["id"]
        try:
            # keep it lightweight if you like:
            word_obj = WordsToAdd.objects.only("id", "word").get(id=word_id)
        except WordsToAdd.DoesNotExist:
            # Will be rendered as a 404 by DRF automatically
            raise NotFound(detail="Word not in WordsToAdd")

        attrs["word_obj"] = word_obj

        # Optional semantic check: syllables must match the word when joined
        syllables = attrs["syllables"]
        if "".join(syllables).lower() != word_obj.word.lower():
            raise ValidationError({"syllables": ["Syllables do not match the word."]})

        return attrs


class WordsToAddViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsToAdd
        fields = ["id", "word", "frequency"]