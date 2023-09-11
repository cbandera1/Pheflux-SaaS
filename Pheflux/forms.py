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
        valid_extensions = ['.csv', '.fpmk', '.txt']
        if not any(geneExp_file.name.endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError("The geneExp file must have csv, fpmk or txt extension")
        return geneExp_file

    def clean_medium_file(self):
        medium_file = self.cleaned_data.get('medium_file')
        valid_extensions = ['.fpmk', '.txt', '.xml', '.csv']
        if not any(medium_file.name.endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError("The medium file must have fpmk, txt, xml or csv extension")
        return medium_file

    def clean_network_file(self):
        network_file = self.cleaned_data.get('network_file')
        if not network_file.name.endswith('.xml'):
            raise forms.ValidationError("The network file must have xml extension")
        return network_file


class SearchBiGGForm(forms.Form):
    query = forms.CharField(
        label="Search network in Bigg Models", max_length=100)


class SearchTCGAForm(forms.Form):
    TCGA_CHOICES = [
        ('Breast', 'Breast'),
        ('Bronchus and lung', 'Bronchus and lung'),
        ('Kidney', 'Kidney'),
    ]
    query = forms.CharField(label="Search GeneExp in TCGA", max_length=100,
                            widget=forms.Select(choices=TCGA_CHOICES))
