
from django import forms
from .models import Product,RequestForProduct,Group

class ProductUploadForm(forms.ModelForm):

    class Meta:
        model=Product
        fields=['name','desc','category']




class CreateRequestForm(forms.ModelForm):

    class Meta:
        model=RequestForProduct
        fields=[
            'product_name',
            'product_desc',
            'request_in_brief',
            'product_category',
            'is_urgent',
            'needed_by',
            'return_date']

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name']