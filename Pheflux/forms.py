from django import forms
import pdb
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class PhefluxForm(forms.Form):
    organism = forms.CharField(label="Organism", max_length=100)
    condition = forms.CharField(label="Condition", max_length=100)
    geneExp_file = forms.FileField(label="geneExp File")
    medium_file = forms.FileField(label="Medium File")
    network_file = forms.FileField(label="Network")
    verbosity = forms.BooleanField(required=True)
    prefix_log_file = forms.CharField(label="Log Prefix", max_length=100)

    def clean_geneExp_file(self):
        geneExp_file = self.cleaned_data.get('geneExp_file')
        if not geneExp_file.name.endswith('.csv') and geneExp_file.name.endswith('.fpmk') and geneExp_file.name.endswith('.txt'):
            raise forms.ValidationError("El archivo debe ser en formato CSV.")
        return geneExp_file

    def clean_medium_file(self):
        medium_file = self.cleaned_data.get('medium_file')
        print(medium_file)
        if not medium_file.name.endswith('.fpmk') and medium_file.name.endswith('.txt') and medium_file.name.endswith('.xml'):
            raise forms.ValidationError("El archivo debe ser en formato FPMK.")
        return medium_file

    def clean_network_file(self):
        medium_file = self.cleaned_data.get('network_file')
        if not medium_file.name.endswith('.xml'):
            raise forms.ValidationError("El archivo debe ser en formato xml.")
        return medium_file


class SearchBiGGForm(forms.Form):
    query = forms.CharField(
        label="Search network in Bigg Models", max_length=100)


class SearchTCGAForm(forms.Form):
    TCGA_CHOICES = [
        ('Breast', 'Breast'),
        ('Bronchus and lung', 'Bronchus and lung'),
        ('Kidney', 'Kidney'),
    ]
    query = forms.CharField(label='TCGA: ', max_length=100,
                            widget=forms.Select(choices=TCGA_CHOICES))
