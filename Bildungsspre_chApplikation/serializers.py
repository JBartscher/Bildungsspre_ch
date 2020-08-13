from abc import ABC

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Description, Field, Word


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FieldSerializer(serializers.HyperlinkedModelSerializer):
    # related = serializers.StringRelatedField(many=True)
    related = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        required=False,
        queryset=Field.objects.all(),
        slug_field='field'
    )

    class Meta:
        model = Field
        fields = ['id', 'url', 'field', 'related']


class DescriptionSerializer(serializers.ModelSerializer):
    # description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    # field = FieldSerializer(many=False, read_only=True)
    # word = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='word_descriptions')

    class Meta:
        model = Description
        fields = ['id', 'url', 'description', 'creation_date', '_order', 'word', 'field']  # '__all__'


class PartialWordSerializer(serializers.ModelSerializer):
    word_descriptions = DescriptionSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Word
        fields = ['url', 'id', 'word', 'related', 'word_descriptions', 'word_type', 'source']


class WordSerializer(serializers.ModelSerializer):
    """ the WordSerialzer uses the DescriptionSerializer which will get us all related objects with the
    many=True Parameter. The Descriptions are by they're model related to a word and a field. It feels
    odd but you dont need to "fetch" the related fields, the framework is doing it recursively like here.
    """
    word_descriptions = DescriptionSerializer(many=True, required=False)

    related = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        required=False,
        queryset=Word.objects.all(),
        slug_field='word'
    )

    class Meta:
        model = Word
        fields = ['url', 'id', 'word', 'related', 'word_descriptions', 'word_type', 'source']
