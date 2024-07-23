from django.forms import ModelForm
from app.models import *
from django import forms

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'workplace']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['title', 'address']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PartnerForm(ModelForm):
    class Meta:
        model = Partner
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }