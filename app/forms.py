from django.forms import ModelForm
from app.models import *
from django import forms

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'contact', 'direction', 'workplace']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'direction': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }
    field_order = ['name', 'contact', 'direction', 'workplace']

class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['title', 'name', 'contact', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

    field_order = ['title', 'name', 'contact', 'address']

class PartnerForm(ModelForm):
    class Meta:
        model = Partner
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }