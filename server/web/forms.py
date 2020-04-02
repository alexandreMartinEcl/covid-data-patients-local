"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django import forms


class RegistrationForm(forms.Form):
    hospital_name = forms.CharField(required=True, label="Nom de l'hopital")
    contact_name = forms.CharField(required=True, label="Nom du responsable")
    address = forms.CharField(required=True, label="Adresse")
    postcode = forms.CharField(required=True, label="Code Postal")
    country = forms.CharField(required=True, initial="France", label="Pays")
    dect = forms.CharField(required=True, label="Numéro DECT Bed Manager")
    contact = forms.EmailField(required=True, label="Adresse email de contact")
