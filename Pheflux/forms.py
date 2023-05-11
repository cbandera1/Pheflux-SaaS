
from django import forms


class PhefluxForm(forms.Form):
    string1 = forms.CharField(label="String 1", max_length=100)
    string2 = forms.CharField(label="String 2", max_length=100)
    csv_file = forms.FileField(label="Archivo CSV")
    fpmk_file = forms.FileField(label="Archivo FPMK")

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo debe ser en formato CSV.")
        return csv_file

    def clean_fpmk_file(self):
        fpmk_file = self.cleaned_data.get('fpmk_file')
        if not fpmk_file.name.endswith('.fpmk'):
            raise forms.ValidationError("El archivo debe ser en formato FPMK.")
        return fpmk_file
