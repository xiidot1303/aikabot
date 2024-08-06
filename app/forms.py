from django.forms import ModelForm
from app.models import *
from django import forms

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'contact', 'direction', 'workplace', 'region']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'direction': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'})
        }
    field_order = ['region', 'name', 'contact', 'direction', 'workplace']

class PharmacyForm(ModelForm):
    class Meta:
        model = Pharmacy
        fields = ['title', 'name', 'name2', 'responsible', 'contact', 'responsible_contact', 'region']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name2': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'})
        }

    field_order = ['region', 'title', 'name', 'name2', 'responsible', 'contact', 'responsible_contact']

class PartnerForm(ModelForm):
    class Meta:
        model = Partner
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }