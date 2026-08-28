from django import forms
from .models import DemandeTirage

class DemandeTirageForm(forms.ModelForm):
    class Meta:
        model = DemandeTirage
        fields = [
            'titre_epreuve',
            'matiere',
            'filiere',
            'niveau',
            'nombre_exemplaires',
            'nombre_pages',
            'fichier_pdf',
            'date_reservation',
            'heure_debut',
        ]
        widgets = {
            'titre_epreuve': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Examen Synthèse'}),
            'matiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Algorithmique'}),
            'filiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: LF-Info'}),
            'niveau': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1ère année'}),
            'nombre_exemplaires': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'nombre_pages': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'fichier_pdf': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}), # Restreint la sélection aux fichiers PDF
            'date_reservation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Affiche un sélecteur de date (calendrier)
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), # Affiche un sélecteur d'heure
        }