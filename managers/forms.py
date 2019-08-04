from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Fieldset, ButtonHolder

from .models import Season, Team


class CustomCheckbox(Field):
    template = 'crispy/custom_checkbox.html'


class CustomInput(Field):
    template = 'crispy/custom_input.html'


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Szukaj', max_length=50)
    

class SeasonCreateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('country', 'name', 'years')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'managers:season-add'
        self.helper.layout = Layout(
            Fieldset('Podstawowe', 'country', 'name', 'years' ),
            ButtonHolder(Submit('submit', 'Zapisz', css_class='my-2'))
        )


class SeasonUpdateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('country', 'name', 'years', 'slug', 'icon_name', 'current', 'date_start', 'date_end', 'jmb_bg1', 'jmb_bg2', 'jmb_col', 'teams')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        country_teams = Team.objects.filter(country=self.instance.country).order_by('-is_national', 'name_full')
        self.fields['teams'] = forms.ModelMultipleChoiceField(
            queryset=country_teams, 
            label="Dodaj drużynę do sezonu",
            required=False
        )
        self.teams_size = len(country_teams)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('managers:season-update', kwargs={ 'slug': self.instance.slug })
        self.helper.layout = Layout(
            Row(
                Column(CustomInput('country'), css_class="form-group col-md-3"),
                Column(CustomInput('name'), css_class="form-group col-md-3"),
                Column(CustomInput('years'), css_class="form-group col-md-2"),
                Column(CustomInput('slug'), css_class="form-group col-md-4"
                )
            ),
            Row(
                CustomCheckbox('current'),
                Column(CustomInput('date_start'), css_class="form-group col-md-2"),
                Column(CustomInput('date_end'), css_class="form-group col-md-2")
            ),
            Row(
                Column(CustomInput('icon_name'), css_class="form-group col-md-4"),
                Column(CustomInput('jmb_bg1'), css_class="form-group col-md-2"),
                Column(CustomInput('jmb_bg2'), css_class="form-group col-md-2"),
                Column(CustomInput('jmb_col'), css_class="form-group col-md-2")
            ),
            Row(
                Column(CustomInput('teams'), css_class="form-group")
            ),
            Submit('submit', 'Zapisz', css_class='my-2')
        )
