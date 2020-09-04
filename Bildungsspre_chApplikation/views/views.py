from django.contrib import messages
from django.views.generic import TemplateView, FormView
from multi_form_view import MultiFormView

from Bildungsspre_chApplikation.forms import WordForm, DescriptionForm
from Bildungsspre_chApplikation.serializers import WordSerializer
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


class NewWordFormView(FormView):
    template_name = "submit_new_word_form_v2.html"

    form_class = WordForm


class WordMultiFormView(MultiFormView):
    form_classes = {
        'word_form': WordForm,
        'description_form': DescriptionForm,
    }

    template_name = 'submit_new_word_form.html'
