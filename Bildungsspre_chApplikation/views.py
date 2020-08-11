from random import random

from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from .serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Word, Field, Description
from .serializers import WordSerializer, FieldSerializer, DescriptionSerializer
from random import randint


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated]


class DescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows descriptions to be viewed or edited.
    """
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class FieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [permissions.IsAuthenticated]

#TODO: filter view for fields

class RandomWordView(APIView):

    queryset = User.objects.none()

    def get(self, request):

        if request.GET.get('field'):
            field = request.GET.get('field')
            self.get_random_with_filter(field)
            print(f'field is: {field}')

        word = self.get_random()

        serializer = WordSerializer(word, context={'request': request})
        return Response(serializer.data)

    #@permission_classes((permissions.AllowAny,))
    def get_random(self):
        max_id = Word.objects.all().aggregate(max_id=Max("id"))['max_id']

        while True:
            pk = randint(1, max_id)

            word = Word.objects.filter(pk=pk).first()

            if word:
                return word

    def get_random_with_filter(self, field):

        try:
            field_obj = Field.objects.get(field__icontains=field)
            print(f"MATCHUING FIELD FOUND: {field_obj.field} id: {field_obj.pk}")

            words = Word.objects.filter(word_descriptions__field_id__exact=field_obj.pk)
            random_pick = randint(0, words.count() - 1)

            return words[random_pick]

        except Field.DoesNotExist:
            field_obj = None
            print("NO MATCHUING FIELD FOUND")
            return self.get_random()
