from bootstrap4.widgets import RadioSelectButtonGroup
from django import forms

from .models import Word, Field, Description
from .widgets import CustomTextInput, CustomTextarea


class DescriptionForm(forms.ModelForm):
    required_css_class = "bootstrap4-req"

    class Meta:
        model = Description

        fields_choices = [(i, j[1]) for i, j in enumerate(Field.objects.all().values_list())]

        fields = ['description', 'field']  # '__all__'
        widgets = {
            "description": CustomTextarea(attrs={"class": "form-control", 'cols': '10', 'rows': '4'}),
            "field": forms.Select(attrs={"class": "form-control"})
        }
        labels = {
            "description": "Erläuterung",
            "field": "Feld"
        }


class WordForm(forms.Form):
    """Form with a variety of widgets to test bootstrap4 rendering."""

    word = forms.CharField(
        max_length=255,
        help_text="Neues Wort",
        required=True,
        widget=CustomTextInput(attrs={"class": "TEST", "placeholder": "Platzhalter"}),
        label="Wort",
    )

    word_type = forms.ChoiceField(
        widget=RadioSelectButtonGroup,
        choices=Word.WORTART_CHOICES,
        help_text="Wortart",
        label="Wortart",
    )

    # get only the names of the fields enumerated for selection
    fields_choices = [(i, j[1]) for i, j in enumerate(Field.objects.all().values_list())]

    # ComboField ?
    # select_field = forms.ChoiceField(choices=fields_choices, help_text="Feld aus dem das Wort kommt", label="Feld")
    # select_field.group = 1
    # description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), strip=False ,label="Erläuterung")
    # description.group = 1

    required_css_class = "bootstrap4-req"

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super().clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data
