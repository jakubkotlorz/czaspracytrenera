from django import forms

from .models import Season, Team


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Szukaj', max_length=50)
    

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

