from django.db import transaction
from .models import Dictionary, WordsToAdd

def add_words_dict_frequency(*,words_to_add):
    from django.db.models import When, Value, Case, IntegerField, F
    with transaction.atomic(savepoint=False):
        if words_to_add:
            existing_words = set(
                Dictionary.objects
                .filter(word__in=words_to_add.keys())
                .values_list("word", flat=True)
            )
            words_that_need_syllables = {
                word: freq
                for word, freq in words_to_add.items()
                if word not in existing_words
            }
            existing = set(
                WordsToAdd.objects.filter(word__in=words_that_need_syllables.keys()).values_list('word', flat=True)
            )
            to_update = {
                word: freq
                for word, freq in words_that_need_syllables.items()
                if word in existing
            }
            if to_update:           
                whens = [When(word=w, then=Value(freq)) for w, freq in to_update.items()]
                WordsToAdd.objects.filter(word__in=to_update.keys()).update(
                    frequency=F('frequency') + Case(*whens, default=Value(0), output_field=IntegerField())
                )

            to_create = {
                word: freq
                for word, freq in words_that_need_syllables.items()
                if word not in existing
            }
            if to_create:
                WordsToAdd.objects.bulk_create(
                    (WordsToAdd(word=word, frequency=freq) for word, freq in to_create.items()),
                    ignore_conflicts=True
                )

def get_word_breaks(*,word_list:list[str]):
    if not word_list:
        return {}
    normalized_unique_words = {word.lower() for word in set(word_list)}
    db_dictionary = Dictionary.objects.filter(word__in=normalized_unique_words).values_list("word","syllable_breaks")
    return {w:breaks for (w, breaks) in db_dictionary}

def check_dictionary_entries(*, word_list: list[str]) -> set[str]:
    from .models import Dictionary
    # Returns the set of words not already in the dictionary.
    if not word_list:
        return set()
    return set(word for word in word_list if word.lower() not in Dictionary.objects.filter(word=word))