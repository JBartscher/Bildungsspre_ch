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
    #related = serializers.StringRelatedField(many=True)
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
    id = serializers.IntegerField(read_only=True)
    field = FieldSerializer(many=True)

    class Meta:
        model = Description

class WordSerializer(serializers.ModelSerializer):

    related = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="related words",
        queryset=Word.objects.all()
    )

    description = serializers.HyperlinkedRelatedField(
        many=True,
        # read_only=True,
        queryset=Description.objects.all(),
        view_name='description'
    )

    class Meta:
        model = Word
        fields = ['word', 'related', 'description']

"""




"""