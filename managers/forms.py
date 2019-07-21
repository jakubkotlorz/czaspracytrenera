from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from .models import Season, Team


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Szukaj', max_length=50)
    

class SeasonCreateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('country', 'name', 'years', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'managers:season-add'
        self.helper.layout = Layout(
            Fieldset('Podstawowe', 'country', 'name', 'years', 'slug' ),
            ButtonHolder(Submit('submit', 'Zapisz', css_class='my-2'))
        )


class SeasonUpdateForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ('country', 'name', 'years', 'slug', 'icon_name', 'current', 'date_start', 'date_end', 'jmb_bg1', 'jmb_bg2', 'jmb_col')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('managers:season-update', kwargs={ 'slug': self.instance.slug })
        self.helper.layout = Layout(
            Fieldset('Podstawowe', 'country', 'name', 'years', 'slug' ),
            Fieldset('Daty', 'current', 'date_start', 'date_end'),
            Fieldset('Wygląd', 'icon_name', 'jmb_bg1', 'jmb_bg2', 'jmb_col'),
            ButtonHolder(Submit('submit', 'Zapisz', css_class='my-2'))
        )


class TeamToSeasonForm(forms.ModelForm):
    class Meta:       
        model = Team
        fields = ()

    def __init__(self, add_team_qs, rem_team_qs, *args, **kwargs):
        super(TeamToSeasonForm, self).__init__(*args, **kwargs)
        self.fields['add_team'] = forms.ModelChoiceField(
            queryset=add_team_qs.order_by('-is_national', 'name_full'), 
            empty_label="Wybierz...",
            label="Dodaj drużynę do sezonu",
            required=False
        )
        self.fields['del_team'] = forms.ModelChoiceField(
            queryset=rem_team_qs.order_by('-is_national', 'name_full'), 
            empty_label="Wybierz...",
            label="Usuń drużynę z sezonu",
            required=False
        )
