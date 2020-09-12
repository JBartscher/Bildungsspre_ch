from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    ADJECTIVE = 'ADJ'
    ADVERB = 'ADV'
    INTERJEKTION = 'INT'
    KONJUNKTION = 'KON'
    PRAEPOSITION = 'PRÄ'
    PRONOMEN = 'PRO'
    SUBSTANTIV = 'SUB'
    VERB = 'VER'

    WORTART_CHOICES = [
        (ADJECTIVE, 'Adjektiv'),
        (ADVERB, 'Adverb'),
        (INTERJEKTION, 'Interjektion'),
        (KONJUNKTION, 'Konjunktion'),
        (PRAEPOSITION, 'Präposition'),
        (PRONOMEN, 'Pronomen'),
        (SUBSTANTIV, 'Substantiv, Nomen'),
        (VERB, 'Verb'),
    ]

    word = models.CharField(max_length=255, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", symmetrical=True, related_name="related_words",
                                     blank=True)  # related words

    word_type = models.CharField(
        max_length=3,
        blank=True,
        choices=WORTART_CHOICES,
        default=SUBSTANTIV,
    )

    source = models.URLField(blank=True)

    user = models.ForeignKey(
        User,
        on_delete=models.SET(1),
        blank=True,
    )

    def __str__(self):
        return f"{self.word}"

    class Meta:
        ordering = ['word']
        verbose_name = 'word'
        verbose_name_plural = 'words'


class Field(models.Model):
    field = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", symmetrical=True, related_name="related_fields",
                                     blank=True)  # related fields

    def __str__(self):
        return f"{self.field}"

    class Meta:
        ordering = ['field']


class Description(models.Model):
    word = models.ForeignKey(Word, related_name="word_descriptions", on_delete=models.CASCADE)
    field = models.ForeignKey(Field, related_name="related_field", default="Bildungssprachlich",
                              on_delete=models.SET_DEFAULT)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.SET(1),
        editable=False,
    )

    class Meta:
        order_with_respect_to = 'word'

    def __str__(self):
        return '%s: %s - %s' % (self.word, self.field, self.description)
