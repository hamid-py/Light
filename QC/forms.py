from django.forms import ModelForm
from django import forms

from .models import SleepyVoice, Voice


class DateInput(forms.DateInput):
    input_type = 'date'


class QcScoreForm(ModelForm):
    class Meta:
        model = SleepyVoice
        fields = ['pass_indicator', 'voice', 'voice_date']
        widgets = {
            'voice_date': DateInput(),
        }

# class QcScoreForm(forms.Form):
#     pass_indicator = forms.BooleanField()
#     voice = forms.ModelChoiceField(queryset=Voice.objects.all())
#     voice_date = forms.DateTimeField(
#         input_formats=['%d/%m/%Y %H:%M'],
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control datetimepicker-input',
#             'data-target': '#datetimepicker1'
#         })
#     )
