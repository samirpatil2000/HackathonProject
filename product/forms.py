
from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import Product,RequestForProduct,Group,CommentTORequest

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
            'date_needed_by',
            'time_needed_by',
            'return_date']

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name']


class CommentForm(forms.ModelForm):
    parent=TreeNodeChoiceField(queryset=CommentTORequest.objects.all())

    # TODO we have to remove required parent field
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # THis for removing the selected option box from comment form
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = CommentTORequest
        fields = ['parent', 'content']