from django.db import models
from django.db.models.functions import Lower

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                               #
#  words that are in the Dictionary.word, WordsToAdd.word and   #
#  Paragraphs.word_set are supposed to be taken as one and are  #
#  not dividet by ' or similiar and also äüß usw. exist in them #
#                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Story(models.Model):
    title = models.CharField(max_length=200)
    teaser = models.TextField()
    author = models.CharField(max_length=100)
    last_updated = models.DateTimeField()
    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=200)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    dictionary_completed = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'order'], name='uq_story_order')
        ]
        ordering = ('story', 'order')
        indexes = [
            models.Index(fields=['story', 'order']),
        ]


    def __str__(self):
        return str(self.order) + ": " + self.title


class Paragraph(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    content = models.TextField()
    dictionary_completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chapter', 'number'], name='uq_chapter_paragraph_number')
        ]
        ordering = ('chapter', 'number')
        indexes = [
            models.Index(fields=['chapter', 'number']),
        ]

    def __str__(self):
        return str(self.number) + " - " + self.chapter.title

class UniqueWordsInParagraph(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='unique_words')
    word = models.TextField(max_length=100)

    class Meta: 
        constraints = [
            models.UniqueConstraint(
                models.F('paragraph'),
                Lower('word'),
                name='uq_paragraph_lower_word',
            ),
        ]
        indexes = [
            # Optional but helpful for case-insensitive lookups
            models.Index(Lower('word'), name='ix_unique_words_word_lower'),
            models.Index(models.F('paragraph'), name='ix_unique_words_paragraph'),
            models.Index(models.F('paragraph'), Lower('word'), name='ix_paragraph_lower_word'),
        ]

    def __str__(self):
        return self.word