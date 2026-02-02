from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Lower

# Create your models here.
class WordsToAdd(models.Model):
    word = models.CharField(max_length=100)
    frequency = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "story_wordstoadd"
        constraints = [
            models.UniqueConstraint(Lower('word'), name='uq_word_lowercase_words_to_add')
        ]
        indexes = [
            models.Index(fields=['-frequency'], name='ix_words_to_add_freq_desc')
        ]

    def __str__(self):
        return self.word
    

class Dictionary(models.Model):
    word = models.CharField(max_length=100)
    syllable_breaks = ArrayField(models.PositiveIntegerField(), default=list)

    class Meta:
        db_table = "story_dictionary"
        constraints = [
            models.UniqueConstraint(Lower('word'), name='uq_word_lowercase_dictionary')
        ]
        
        indexes = [
            models.Index(Lower('word'), name='ix_dictionary_word_lower'),  # optional but recommended
        ]

    def __str__(self):
        return self.word