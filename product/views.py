from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductUploadForm
# Create your views here.

def index(request):
    context={

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
            return redirect('index-page')
    context={
        'form':productForm
    }
    return render(request,'product/productUploadForm.html',context)
