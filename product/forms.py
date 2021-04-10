
from django import forms
from .models import Product,RequestForProduct

class ProductUploadForm(forms.ModelForm):

    class Meta:
        model=Product
        fields=['name','desc','category']
