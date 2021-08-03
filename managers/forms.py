from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, Field, Fieldset, ButtonHolder

from .models import Season, Team, Employment


class CustomCheckbox(Field):
    template = 'crispy/custom_checkbox.html'


class CustomInput(Field):
    template = 'crispy/custom_input.html'


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Szukaj', max_length=50)


class EndJobDateForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ('date_finish', )
        widgets = {
            'date_finish': forms.DateInput(attrs={'type': 'date'})
        }


class TeamAddJobForm(forms.ModelForm):
    """Model form to add new employment."""
    class Meta:
        model = Employment
        exclude = ('team', )
        widgets = {
            'manager': forms.Select(attrs={'id': 'selected_manager'}),
            'date_start': forms.DateInput(attrs={'type': 'date'}, ),
            'date_finish': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            CustomInput('manager', css_class='form-group mb-3'),
            Row(
                Column(CustomInput('role'), css_class='form-group col-md-2 mb-0'),
                Column(CustomInput('date_start'), css_class='form-group col-md-4 mb-0'),
                Column(CustomInput('date_finish'), css_class='form-group col-md-4 mb-0'),
                Column(CustomInput('still_hired'), css_class='form-group col-md-2 mb-0'),
                css_class = 'form-row mb-5'
            ),
            ButtonHolder(
                Submit('add', 'Dodaj', css_class='btn btn-success mr-1 ml-2'),
                Button('cancel', 'Anuluj', css_class='btn btn-danger mr-1 ml-2', onclick="javascript:history.back();"),
                css_class='my-3'
            )
        )
    

class SeasonCreateForm(forms.ModelForm):
    """Model form to create new season."""
    class Meta:
        model = Season
        fields = ('country', 'name', 'years')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('Podstawowe', 'country', 'name', 'years' ),
            ButtonHolder(Submit('submit', 'Zapisz', css_class='my-2'))
        )


class SeasonAvanceForm(forms.ModelForm):
    """Model form to show values of last season and make it possible to edit and save as new one."""
    last_season_teams = forms.ModelMultipleChoiceField(
        queryset = None,
        required = False
    )
    considered_teams = forms.ModelMultipleChoiceField(
        queryset = None,
        required = False
    )

    class Meta:
        model = Season
        fields = ('name', 'years', 'date_start', 'date_end', 'slug')

    def __init__(self, *args, **kwargs):
        self.previous_teams = kwargs.pop('previous_teams')
        self.possible_teams = kwargs.pop('possible_teams')
        self.slug = kwargs.pop('slug')
        super(SeasonAvanceForm, self).__init__(*args, **kwargs)

        self.fields['last_season_teams'].queryset = self.previous_teams
        self.fields['last_season_teams'].widget.attrs['size'] = str(len(self.previous_teams))
        self.fields['considered_teams'].queryset = self.possible_teams
        self.fields['considered_teams'].widget.attrs['size'] = str(len(self.previous_teams))

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('managers:season-avance', kwargs={ 'slug': self.slug })
        self.helper.layout = Layout(
            Row(
                Column(CustomInput('name'), css_class="form-group col-md-7"),
                Column(CustomInput('years'), css_class="form-group col-md-5"),
            ),
            Row(
                Column(CustomInput('date_start'), css_class="form-group col-md-6"),
                Column(CustomInput('date_end'), css_class="form-group col-md-6"),
            ),
            Row(
                Column(CustomInput('last_season_teams'), css_class="form-group col-md-6 chosen"),
                Column(CustomInput('considered_teams'), css_class="form-group col-md-6 chosen"),
            ),
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


class UploadFileForm(forms.Form):
    file = forms.FileField(
        widget = forms.FileInput(
            attrs = {
                'class': 'custom-file-input',
                'id': 'customFile',
                'name': 'givenFile'
            }
        )
    )

class WikipediaTextForm(forms.Form):
    wikiInput = forms.CharField(
        widget = forms.Textarea(
            attrs = {
                'id': 'wikiTextArea',
                'class': 'form-control',
                'rows': 5
            }
        )
    )
