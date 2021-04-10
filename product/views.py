from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductUploadForm,CreateRequestForm
from .models import RequestForProduct
# Create your views here.


def index(request):
    context={
        'objects':RequestForProduct.objects.filter(is_submitted=False)
    }
    return render(request,'product/index.html',context)


@login_required
def uploadProduct(request):
    user=request.user
    productForm=ProductUploadForm()
    if request.method=="POST":
        productForm=ProductUploadForm(request.POST or None)
        if productForm.is_valid():
            prod=productForm.save(commit=False)
            prod.user=user
            prod.save()
            return redirect('index-page')
    context={
        'form':productForm
    }
    return render(request,'product/productUploadForm.html',context)


@login_required
def create_product_request(request):
    user=request.user
    requestForm=CreateRequestForm()
    if request.method=="POST":
        requestForm=CreateRequestForm(request.POST or None)
        if requestForm.is_valid():
            prod_request=requestForm.save(commit=False)
            prod_request.user=user
            prod_request.save()
            return redirect('index-page')
    context={
        'form':requestForm
    }
    return render(request,'product/createRequestForm.html',context)
