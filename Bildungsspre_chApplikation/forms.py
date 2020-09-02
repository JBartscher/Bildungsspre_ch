
from django import forms
from django.forms import BaseFormSet, formset_factory
from django.forms.forms import BaseForm

from .models import Word, Field, Description

from bootstrap4.widgets import RadioSelectButtonGroup

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['description', 'field'] # '__all__'
        widgets = {
            "description" : forms.Textarea(attrs={"class" : "description", 'cols': '10', 'rows': '4'}),
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
        widget=forms.TextInput(attrs={"placeholder": "Platzhalter"}),
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
    # description = forms.CharField(widget=forms.Textarea, strip=False ,label="Erläuterung")
    # description.group = 1

    required_css_class = "bootstrap4-req"

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super().clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data

class NewDescriptionFormSet(BaseFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        # form.nested = DescriptionForm()

    def clean(self):
        super().clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

class NewWordFormSet(BaseFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = NewDescriptionFormSet(
            #instance=form.instance,
            #data=form.data if form.is_bound else None,
            #files=form.files if form.is_bound else None,
            #extra=1
        )

    def clean(self):
        super().clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

NewWordFormSet = formset_factory(WordForm, formset=NewWordFormSet, extra=1)
NewDescriptionFormSet = formset_factory(DescriptionForm, formset=NewDescriptionFormSet, extra=1, max_num=10, validate_max=True)

class EmptyForm(BaseForm):
    pass
