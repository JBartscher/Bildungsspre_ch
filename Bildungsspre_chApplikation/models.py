from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self")  # related words

    class Meta:
        ordering = ['word']


class Field(models.Model):
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self")  # related fields

    class Meta:
        ordering = ['title']

class Description(models.Model):
    field = models.ForeignKey(Field, default="Wissenschaftlich", on_delete=models.SET_DEFAULT)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'word'
