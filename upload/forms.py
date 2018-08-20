from django import forms

from .models import Dataset


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ('dataset_name', 'document',)
