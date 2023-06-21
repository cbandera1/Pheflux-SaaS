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
            raise forms.ValidationError("El archivo debe ser en formato xml.")
        return medium_file


class SearchBiGGForm(forms.Form):
    query = forms.CharField(label='BiGG', max_length=100)


class SearchTCGAForm(forms.Form):
    TCGA_CHOICES = [
        ('Accessory sinuses', 'Accessory sinuses'),
        ('Adrenal gland', 'Adrenal gland'),
        ('Anus and anal canal', 'Anus and anal canal'),
        ('Base of tongue', 'Base of tongue'),
        ('Bladder', 'Bladder'),
        ('Bones, joints and articular cartilage of limbs',
         'Bones, joints and articular cartilage of limbs'),
        ('Bones, joints and articular cartilage of other and unspecified sites',
         'Bones, joints and articular cartilage of other and unspecified sites'),
        ('Brain', 'Brain'),
        ('Breast', 'Breast'),
        ('Bronchus and lung', 'Bronchus and lung'),
        ('Cervix uteri', 'Cervix uteri'),
        ('Colon', 'Colon'),
        ('Connective, subcutaneous and other soft tissues',
         'Connective, subcutaneous and other soft tissues'),
        ('Corpus uteri', 'Corpus uteri'),
        ('Esophagus', 'Esophagus'),
        ('Eye and adnexa', 'Eye and adnexa'),
        ('Floor of mouth', 'Floor of mouth'),
        ('Gallbladder', 'Gallbladder'),
        ('Gum', 'Gum'),
        ('Heart, mediastinum, and pleura', 'Heart, mediastinum, and pleura'),
        ('Hematopoietic and reticuloendothelial systems',
         'Hematopoietic and reticuloendothelial systems'),
        ('Hypopharynx', 'Hypopharynx'),
        ('Kidney', 'Kidney'),
        ('Larynx', 'Larynx'),
        ('Lip', 'Lip'),
        ('Liver and intrahepatic bile ducts', 'Liver and intrahepatic bile ducts'),
        ('Lymph nodes', 'Lymph nodes'),
        ('Meninges', 'Meninges'),
        ('Nasal cavity and middle ear', 'Nasal cavity and middle ear'),
        ('Nasopharynx', 'Nasopharynx'),
        ('Oropharynx', 'Oropharynx'),
        ('Other and ill-defined digestive organs',
         'Other and ill-defined digestive organs'),
        ('Other and ill-defined sites', 'Other and ill-defined sites'),
        ('Other and ill-defined sites in lip, oral cavity and pharynx',
         'Other and ill-defined sites in lip, oral cavity and pharynx'),
        ('Other and ill-defined sites within respiratory system and intrathoracic organs',
         'Other and ill-defined sites within respiratory system and intrathoracic organs'),
        ('Other and unspecified female genital organs',
         'Other and unspecified female genital organs'),
        ('Other and unspecified major salivary glands',
         'Other and unspecified major salivary glands'),
        ('Other and unspecified male genital organs',
         'Other and unspecified male genital organs'),
        ('Other and unspecified parts of biliary tract',
         'Other and unspecified parts of biliary tract'),
        ('Other and unspecified parts of mouth',
         'Other and unspecified parts of mouth'),
        ('Other and unspecified parts of tongue',
         'Other and unspecified parts of tongue'),
        ('Other and unspecified urinary organs',
         'Other and unspecified urinary organs'),
        ('Other endocrine glands and related structures',
         'Other endocrine glands and related structures'),
        ('Ovary', 'Ovary'),
        ('Palate', 'Palate'),
        ('Pancreas', 'Pancreas'),
        ('Parotid gland', 'Parotid gland'),
        ('Penis', 'Penis'),
        ('Peripheral nerves and autonomic nervous system',
         'Peripheral nerves and autonomic nervous system'),
        ('Placenta', 'Placenta'),
        ('Prostate gland', 'Prostate gland'),
        ('Pyriform sinus', 'Pyriform sinus'),
        ('Rectosigmoid junction', 'Rectosigmoid junction'),
        ('Rectum', 'Rectum'),
        ('Renal pelvis', 'Renal pelvis'),
        ('Retroperitoneum and peritoneum', 'Retroperitoneum and peritoneum'),
        ('Skin', 'Skin'),
        ('Small intestine', 'Small intestine'),
        ('Spinal cord, cranial nerves, and other parts of central nervous system',
         'Spinal cord, cranial nerves, and other parts of central nervous system'),
        ('Stomach', 'Stomach'),
        ('Testis', 'Testis'),
        ('Thymus', 'Thymus'),
        ('Thyroid gland', 'Thyroid gland'),
        ('Tonsil', 'Tonsil'),
        ('Trachea', 'Trachea'),
        ('Ureter', 'Ureter'),
        ('Uterus, NOS', 'Uterus, NOS'),
        ('Vagina', 'Vagina'),
        ('Vulva', 'Vulva'),
        ('Unknown', 'Unknown'),
        ('Not Reported', 'Not Reported'),
        ('Not Applicable', 'Not Applicable'),
    ]
    query = forms.CharField(label='TCGA', max_length=100,
                            widget=forms.Select(choices=TCGA_CHOICES))
