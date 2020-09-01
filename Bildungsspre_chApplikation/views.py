from random import random

from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.serializers import serialize as django_serialize
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import UserSerializer, GroupSerializer, PartialWordSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Word, Field, Description
from .serializers import WordSerializer, FieldSerializer, DescriptionSerializer
from random import randint


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

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows descriptions to be viewed or edited.
    """
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FieldViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = Field.objects.all()
    serializer_class = FieldSerializer



# TODO: filter view for fields

class RandomWordView(TemplateView):

    template_name = "random.html"

    def get(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)

        if request.GET.get('field'):
            field = request.GET.get('field')
            word = get_random_with_filter(field)
            print(f'field is: {field}')
        else:
            word = get_random()

        serializer = WordSerializer(word, context={'request': request})
        # append the serialized word to the request context so it can be displayed in template the view
        context["word"] = serializer.data

        messages.debug(request, serializer.data)
        return self.render_to_response(context)

class RandomWordAPIView(APIView):
    queryset = User.objects.none()

    def get(self, request):

        if request.GET.get('field'):
            field = request.GET.get('field')
            word = get_random_with_filter(field)
            print(f'field is: {field}')
        else:
            word = get_random()

        serializer = WordSerializer(word, context={'request': request})
        return Response(serializer.data)

    # @permission_classes((permissions.AllowAny,))

class CreateWordCompleteView(APIView):
    # TODO: only authenticated users
    queryset = User.objects.none()

    def _get_field_pk_from_field_name(self, field_name):
        field_obj = Field.objects.get(field__icontains=field_name)
        return field_obj.pk

    def _replace_field_names_with_field_pks(self, data):
        """
        replaces names of fields in POST data with a pk if the field is not alphanumeric.
        TODO: check if already alphanumeric and is valid field

        :param data: the POST data
        :return: replaces name of field with pk of field.
        Example:
        BEFORE: {'word': 'sublim', 'related': [], 'word_descriptions': [{'description': 'nur mit großer Feinsinnigkeit wahrnehmbar, verständlich; nur einem sehr feinen Verständnis, Empfinden zugänglich', 'field': 'bildungssprachlich'}], 'word_type': 'ADJ', 'source': ''}
        AFTER: {'word': 'sublim', 'related': [], 'word_descriptions': [{'description': 'nur mit großer Feinsinnigkeit wahrnehmbar, verständlich; nur einem sehr feinen Verständnis, Empfinden zugänglich', 'field': 4}], 'word_type': 'ADJ', 'source': ''}
        """
        for description in data.get('word_descriptions'):
            if type(description) != dict:
                return Response("all entries in word_description need to be a description-dictionary",
                                status=status.HTTP_400_BAD_REQUEST)

            if not description.get("field").isnumeric():
                # replace field name with pk of field to make it serializable
                description["field"] = self._get_field_pk_from_field_name(
                    description.get("field", "Bildungssprachlich"))

        return data

    @permission_classes(permissions.IsAuthenticated, )
    def post(self, request, format=None):
        data = request.data

        if 'word' not in data or 'word_descriptions' not in data:
            return Response("missing key: 'word' or 'word_description' not provided",
                            status=status.HTTP_400_BAD_REQUEST)

        data = self._replace_field_names_with_field_pks(data)

        try:
            word_serializer = PartialWordSerializer(data=data, context={'request': request},
                                                    partial=True)  # , partial=True
            if word_serializer.is_valid():
                word_serializer.save()

                for description in data.get('word_descriptions'):
                    description["word"] = word_serializer.data.get('id')

                    description_serializer = DescriptionSerializer(data=description, context={'request': request})

                    if description_serializer.is_valid():
                        description_serializer.save()
                    else:
                        return Response(description_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                """
                pk = word_serializer.data.get('id')
                 
                try:
                    word = Word.objects.get(pk=pk)
                    _ = django_serialize('json', [word], cls=DjangoJSONEncoder)
                    _ = _[1:-1]
                    print(_)
                except Exception as e:
                    print(e)

                word_serializer.validated_data
                
                serializer = PartialWordSerializer(word_serializer.data, data={'word_descriptions': data.get('word_descriptions')}, context={'request': request}, partial=True)
                serializer.is_valid()
                print(serializer.errors)
                print(serializer.data)
                
                """


                return Response(word_serializer.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(word_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # new_word = self.create_word_from_request_data(data)
            # new_word.save()
        except Exception as ex:
            # new_word.delete()
            return Response(f"cannot create word {ex}", status=status.HTTP_400_BAD_REQUEST)

        # return Response(status=status.HTTP_202_ACCEPTED)

# if word.is_valid():
#
# return Response("OK", status=status.HTTP_200_OK)
# return Response(word.errors, status=status.HTTP_400_BAD_REQUEST)


# serializer = SnippetSerializer(data=request.data)
# if serializer.is_valid():
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
