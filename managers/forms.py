from django import forms

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Szukaj', max_length=50)
    