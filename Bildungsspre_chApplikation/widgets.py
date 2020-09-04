from django.forms.widgets import (
    TextInput,
    Textarea
)


class CustomTextInput(TextInput):
    template_name = 'widgets/custom_text_input.html'

    def __init__(self, attrs=None, *args, **kwargs):
        attrs["class"] = "test"
        super().__init__(attrs)


class CustomTextarea(Textarea):
    template_name = 'widgets/custom_text_area.html'
