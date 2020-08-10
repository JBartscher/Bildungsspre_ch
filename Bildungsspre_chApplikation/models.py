from django.db import models


class Word(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateField()


class Field(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    description = models.TextField()
