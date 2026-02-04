from rest_framework.generics import ListAPIView #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework.views import APIView #type: ignore
from rest_framework import status #type:ignore

from django.db import transaction
from .serializers import WordsToAddViewSerializer, CandidatesToDictionarySerializer

from dictionary.helper.word import syllable_list_to_breaks as svc_list_to_breaks
from .models import WordsToAdd, Dictionary

# Create your views here.
class CandidatesToDictionary(APIView):
    """
    POST JSON:
    {
      "id": 123,
      "syllables": ["hel", "lo"]
    }
    """
    def post(self, request):
        serializer = CandidatesToDictionarySerializer(data=request.data)
        # We want a consistent 400 body with {"errors": {...}}
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        word_obj = serializer.validated_data["word_obj"]
        syllables = serializer.validated_data["syllables"]

        # Compute breaks (e.g., ["hel","lo"] -> [3])
        syllable_breaks = svc_list_to_breaks(syllables)

        # Perform the move atomically and with a row lock
        with transaction.atomic():
            # lock the row at the last moment to avoid races
            w = WordsToAdd.objects.select_for_update().get(pk=word_obj.pk)
            d = Dictionary.objects.create(
                word=w.word,
                syllable_breaks=syllable_breaks
            )
            w.delete()

        return Response(
            {"word": d.word, "syllable_breaks": d.syllable_breaks},
            status=status.HTTP_200_OK
        )


class WordsToAddView(ListAPIView):
    serializer_class = WordsToAddViewSerializer
    pagination_class = None

    def get_queryset(self):
        params = self.request.query_params
        qs = WordsToAdd.objects.order_by("-frequency")

        prefix = params.get("prefix")
        if prefix:
            qs.filter(word__istartswith=prefix)

        limit = params.get("limit")
        if limit and limit.isdigit():
            return qs[: int(limit)]
        return qs[:10]
