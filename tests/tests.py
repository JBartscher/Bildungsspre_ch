from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from Bildungsspre_chApplikation.models import Word, Field, Description
from Bildungsspre_chApplikation.views import view_utils


class ViewUtilsTest(TestCase):
    def setUp(self):
        # create text fixture
        self.user = User.objects.create_user(
            username='joe', email='joe@…', password='plaintextpasswordsinproductionarebad')

        self.word_obj1 = Word.objects.create(word="Testword_1", creation_date=datetime.now(), user_id=1)
        Word.objects.create(word="Testword_2", creation_date=datetime.now(), user_id=1)
        Word.objects.create(word="Testword_3", creation_date=datetime.now(), user_id=1)

        self.field_obj1 = Field.objects.create(field="Testfield_1", creation_date=datetime.now())
        self.field_obj2 = Field.objects.create(field="Testfield_2", creation_date=datetime.now())

        Description.objects.create(word=self.word_obj1, field=self.field_obj1, creation_date=datetime.now(),
                                   description="TEST", user_id=1)

    def test_rand_word(self):
        test_word = view_utils.get_random()
        self.assertIsNotNone(test_word)

    def test_rand_word_with_filter(self):
        test_word = view_utils.get_random_with_filter("Testfield_1")
        self.assertIsNotNone(test_word)
