from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Field, ButtonHolder, Submit

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
        fields = ('country', 'name', 'years', 'slug', 'icon_name', 'current', 'date_start', 'date_end', 'jmb_bg1', 'jmb_bg2', 'jmb_col', 'teams')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teams'] = forms.ModelMultipleChoiceField(
            queryset=Team.objects.filter(country=self.instance.country).order_by('-is_national', 'name_full'), 
            label="Dodaj drużynę do sezonu",
            required=False
        )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('managers:season-update', kwargs={ 'slug': self.instance.slug })
        self.helper.layout = Fieldset(
            Field('country'),
            Field('name'),
            Field('years', css_class="form-group col-md-2 "),
            Field('slug', wrapper_class="form-group col-md-4 "),
            Field('current', css_class="form-group col-md-2 "),
            Field('date_start', css_class="form-group col-md-3 "),
            Field('date_end', css_class="form-group col-md-3 "),
            Field('icon_name', css_class="form-group col-md-3 "),
            Field('jmb_bg1', css_class="form-group col-md-3 "),
            Field('jmb_bg2', css_class="form-group col-md-3 "),
            Field('jmb_col', css_class="form-group col-md-3 "),
            Field('teams', css_class="form-group col-md-12 "),

            Submit('submit', 'Zapisz', css_class='my-2')
        )


# class TeamToSeasonForm(forms.ModelForm):
#     class Meta:       
#         model = Team
#         fields = ()

#     def __init__(self, add_team_qs, rem_team_qs, *args, **kwargs):
#         super(TeamToSeasonForm, self).__init__(*args, **kwargs)
#         self.fields['add_team'] = forms.ModelChoiceField(
#             queryset=add_team_qs.order_by('-is_national', 'name_full'), 
#             empty_label="Wybierz...",
#             label="Dodaj drużynę do sezonu",
#             required=False
#         )
#         self.fields['del_team'] = forms.ModelChoiceField(
#             queryset=rem_team_qs.order_by('-is_national', 'name_full'), 
#             empty_label="Wybierz...",
#             label="Usuń drużynę z sezonu",
#             required=False
#         )
