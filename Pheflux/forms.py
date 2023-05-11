from django import forms
from .utils.phefluxParser import *


class PhefluxForm(forms.Form):
    organism = forms.CharField(label="Organism", max_length=100)
    condition = forms.CharField(label="Condition", max_length=100)
    geneExp_file = forms.FileField(label="Archivo CSV")
    medium_file = forms.FileField(label="Archivo FPMK")
    verbosity = forms.BooleanField(required=True)
    prefix_log_file = forms.CharField(label="Log Prefix", max_length=100)

    def clean_csv_file(self):
        geneExp_file = self.cleaned_data.get('csv_file')
        if not geneExp_file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo debe ser en formato CSV.")
        return geneExp_file

    def clean_fpmk_file(self):
        medium_file = self.cleaned_data.get('fpmk_file')
        if not medium_file.name.endswith('.fpmk'):
            raise forms.ValidationError("El archivo debe ser en formato FPMK.")
        return medium_file
