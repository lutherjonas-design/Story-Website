from django.db import models

# Create your models here.
class wordsToAdd(models.Model):
    word = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.word
    

class dictionary(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    syllables = models.CharField(max_length=200)

    def __str__(self):
        return self.word


class Storys(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title


class Chapters(models.Model):
    title = models.CharField(max_length=200)
    story = models.ForeignKey(Storys, on_delete=models.CASCADE)
    number = models.IntegerField()
    content = models.TextField()
    
    def __str__(self):
        return str(self.number) + self.title


class paragraphs(models.Model):
    Chapters = models.ForeignKey(Chapters, on_delete=models.CASCADE)
    number = models.IntegerField()
    content = models.TextField()

    def __str__(self):
        return str(self.number) + " - " + self.Chapters.title