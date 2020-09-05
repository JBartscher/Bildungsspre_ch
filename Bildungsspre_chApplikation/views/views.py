from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from multi_form_view import MultiFormView
from rest_framework import status

from Bildungsspre_chApplikation.forms import WordForm, DescriptionForm
from Bildungsspre_chApplikation.models import Word
from Bildungsspre_chApplikation.serializers import WordSerializer, PartialWordSerializer, DescriptionSerializer
from Bildungsspre_chApplikation.views.view_utils import get_random, get_random_with_filter


class RandomWordView(TemplateView):
    """ render a random word as a view"""

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


class WordMultiFormView(MultiFormView):
    form_classes = {
        'word_form': WordForm,
        'description_form': DescriptionForm,
    }

    template_name = 'submit_new_word_form.html'

    def post(self, request, **kwargs):

        data = request.POST

        fields = request.POST.getlist('field')
        descriptions = request.POST.getlist('description')

        word_descriptions = []

        for field, description in zip(fields, descriptions):
            word_descriptions.append({'field': field, 'description': description, 'word': None})

        print(word_descriptions)

        data = {'word': request.POST.get('word'),
                'word_type': request.POST.get('word_type'),
                'source': '',
                'word_descriptions': word_descriptions,
                }

        print(data)

        # if 'word' not in data or 'word_descriptions' not in data:
        #    return Response("missing key: 'word' or 'word_description' not provided",
        #                    status=status.HTTP_400_BAD_REQUEST)

        try:

            word_serializer = PartialWordSerializer(data=data, context={'request': request},
                                                    partial=True)  # , partial=True
            if word_serializer.is_valid():
                word_serializer.save()
            else:
                return HttpResponse(word_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for description in data.get('word_descriptions'):

                word = word_serializer.data.get('id')
                description["word"] = word

                description_serializer = DescriptionSerializer(data=description, context={'request': request})

                if description_serializer.is_valid():
                    description_serializer.save()
                else:
                    return HttpResponse(description_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            messages.info(request, str(Word.objects.all().filter(pk=word_serializer.data.get('id'))))

            return redirect('/new')

        except Exception as ex:
            # new_word.delete()
            print(f'EXCEPTION: {ex}')
            return HttpResponse(f"cannot create word {ex}", status=status.HTTP_400_BAD_REQUEST)

        # return HttpResponse(x)
