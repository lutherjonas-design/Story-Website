from django.db import transaction
from .models import Dictionary, WordsToAdd

def add_words(*,words:list[str]):
    with transaction.atomic(savepoint=False):
        for word in words:
            if not Dictionary.objects.filter(word=word).first:
                if not WordsToAdd.objects.filter(word=word).first:
                    WordsToAdd.objects.create(words)