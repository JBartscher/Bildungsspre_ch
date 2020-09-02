from random import randint

from django.db.models import Max

from Bildungsspre_chApplikation.models import Word, Field


def get_random():
    max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id']

    while True:
        pk = randint(1, max_id)

        word = Word.objects.filter(pk=pk).first()

        if word:
            return word


def get_random_with_filter(field):

    try:

        if field.isdecimal() == True:
            field_obj = Field.objects.get(pk=int(field))
        else:
            field_obj = Field.objects.get(field__icontains=field)
        print(f"MATCHUING FIELD FOUND: {field_obj.field} id: {field_obj.pk}")

        words = Word.objects.filter(word_descriptions__field_id__exact=field_obj.pk)
        random_pick = randint(0, words.count() - 1)

        return words[random_pick]

    except Field.DoesNotExist:
        field_obj = None
        print("NO MATCHUING FIELD FOUND")
        return get_random()