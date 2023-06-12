from django import forms
import pdb


class PhefluxForm(forms.Form):
    organism = forms.CharField(label="Organism", max_length=100)
    condition = forms.CharField(label="Condition", max_length=100)
    geneExp_file = forms.FileField(label="Archivo geneExp")
    medium_file = forms.FileField(label="Archivo Medium")
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
            raise forms.ValidationError("El archivo debe ser en formato FPMK.")
        return medium_file


class SearchBiGGForm(forms.Form):
    query = forms.CharField(label='Query', max_length=100)


class SearchTCGAForm(forms.Form):
    query = forms.CharField(label='Query', max_length=100)

    # selected_items = forms.ChoiceField(choices=[])
    # print(selected_items)

    # def __init__(self, options, *args, **kwargs):
    #     super(BiggModelDownload, self).__init__(*args, **kwargs)
    #     self.fields['selected_items'].choices = [
    #         (item, item) for item in options]

    # def clean_selected_items(self):
    #     selected_value = self.cleaned_data['selected_items']
    #     codigo = selected_value.split()[0]
    #     return codigo
