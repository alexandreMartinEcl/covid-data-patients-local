from django import forms

class RegistrationForm(forms.Form):
    hospital_name = forms.CharField(required=True, label="Nom de l'hopital")
    contact_name = forms.CharField(required=True, label="Nom du responsable")
    address = forms.CharField(required=True, label="Adresse")
    postcode = forms.CharField(required=True, label="Code Postal")
    country = forms.CharField(required=True, initial="France", label="Pays")
    dect = forms.CharField(required=True, label="Numéro DECT Bed Manager")
    contact = forms.EmailField(required=True, label="Adresse email de contact")

