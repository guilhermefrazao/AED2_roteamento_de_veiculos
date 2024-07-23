from django import forms
from .models import AlgorithmParameters

class AlgorithmParametersForm(forms.ModelForm):
    class Meta:
        model = AlgorithmParameters
        fields = '__all__'
