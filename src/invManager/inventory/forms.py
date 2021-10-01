from django import forms
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.forms import Form
from .models import Product, Vendor

class ProductForm(forms.ModelForm):
    # vendor = forms.ModelChoiceField(queryset=Product.objects.all().values_list('name'))
    id = forms.CharField(label = "",required=True, widget=forms.TextInput(
        attrs={"placeholder":"ID", "class":"form-control"}
    ))
    name = forms.CharField(label = "", required=True, widget=forms.TextInput(
        attrs={"placeholder": "Name", "class":"form-control"}
    ))
    upc_code = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs = {"placeholder":"UPC Code", "class":"form-control"}
    ))
    count = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs = {"placeholder":"Count", "class":"form-control"}
    ))
    vendor = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs = {"placeholder":"Vendor", "class":"form-control"}
    ))
    class Meta:
        model = Product
        fields =[
            'id',
            'name',
            'upc_code',
            'count',
            'vendor'
        ]


class VendorForm(forms.ModelForm):
    # vendor = forms.ModelChoiceField(queryset=Product.objects.all().values_list('name'))
    id = forms.CharField(label = "",required=True, widget=forms.TextInput(
        attrs={"placeholder":"ID", "class":"form-control"}
    ))
    name = forms.CharField(label = "", required=True, widget=forms.TextInput(
        attrs={"placeholder": "Name", "class":"form-control"}
    ))
    address = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs = {"placeholder":"UPC Code", "class":"form-control"}
    ))
    class Meta:
        model = Vendor
        fields =[
            'id',
            'name',
            'address',
        ]

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class' :'form-control', 'label':"Select Excel file to import"}))
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = "Select Excel file to import"


class CreatePurchaseOrderForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder":"Search", "class": "form-control"}
    ))

class DateForm(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date',"class": "form-control date-form"}))
    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = ""

