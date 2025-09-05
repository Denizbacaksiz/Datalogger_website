from django import forms
from django.forms.widgets import DateTimeInput

class DateFilter(forms.Form):
    start_datetime = forms.DateTimeField(
        widget=DateTimeInput(attrs={
        'type': 'datetime-local',
        'style': 'padding: 8px; border: 1px solid #ddd; border-radius: 5px;'
    }),
        required=False ,
        input_formats=['%Y-%m-%dT%H:%M'],
        label = "Başlangıç Tarihi"
    )

    end_datetime = forms.DateTimeField(
        widget=DateTimeInput(attrs={
            'type': 'datetime-local',
            'style': 'padding: 8px; border: 1px solid #ddd; border-radius: 5px;'
        }),
        required= False ,
        input_formats=['%Y-%m-%dT%H:%M'],
        label = "Bitiş Tarihi"
    )