from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    related = models.ManyToManyField("self", symmetrical=True, related_name="related_words",
                                     blank=True)  # related words

    ADJECTIVE = 'ADJ'
    ADVERB = 'ADV'
    INTERJEKTION = 'INT'
    KONJUNKTION = 'KON'
    PRÄPOSITION = 'PRÄ'
    PRONOMEN = 'PRO'
    SUBSTANTIV = 'SUB'
    VERB = 'VER'

    WORTART_CHOICES = [
        (ADJECTIVE, 'Adjective'),
        (ADVERB, 'Adverb'),
        (INTERJEKTION, 'Interjection'),
        (KONJUNKTION, 'Konjunktion'),
        (PRÄPOSITION, 'Präposition'),
        (PRONOMEN, 'Pronomen'),
        (SUBSTANTIV, 'Substantiv, Nomen'),
        (VERB, 'Verb'),
    ]
    word_type = models.CharField(
        max_length=3,
        blank=True,
        choices=WORTART_CHOICES,
        default=SUBSTANTIV,
    )

    source = models.URLField(blank=True)

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

    class Meta:
        order_with_respect_to = 'word'

    def __str__(self):
        return '%s: %s - %s' % (self.word, self.field, self.description)
