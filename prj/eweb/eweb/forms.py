
from django import forms
 
# import Model from models.py
from .models import Customer
 
# create a ModelForm
class CustForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ('date','bal',)