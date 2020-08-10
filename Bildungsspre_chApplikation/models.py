from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", related_name="related_words", blank=True)  # related words

    class Meta:
        ordering = ['word']


class Field(models.Model):
    field = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", related_name="related_fields", blank=True)  # related fields

    def __str__(self):
        return f"{self.field}"

    class Meta:
        ordering = ['field']


class Description(models.Model):
    field = models.ForeignKey(Field, related_name="fields", default="Wissenschaftlich", on_delete=models.SET_DEFAULT)
    word = models.ForeignKey(Word, related_name="words", on_delete=models.CASCADE)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'word'

    def __str__(self):
        return '%s: %s - %s' % (self.word, self.field, self.description)
