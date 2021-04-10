from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProductUploadForm,CreateRequestForm
from .models import RequestForProduct,Product,Group
from django.contrib import messages
# Create your views here.


def index(request):
    context={
        'objects':RequestForProduct.objects.filter(is_submitted=False)
    }
    # return render(request,'product/index.html',context)
    if request.user.is_authenticated:
        if not request.user.group:
            messages.warning(request,'Please Join Your Respected Group.!')
    else:
        messages.warning(request, 'Please Kindly Log In.!')

    return render(request,'main/index.html',context)


def requestListPage(request):
    context = {
        'objects': RequestForProduct.objects.filter(is_submitted=False)
    }
    return render(request, 'main/request_list.html', context)

def requestDetailView(request,id):
    context={
        'object':RequestForProduct.objects.get(id=id)
    }
    return render(request,'main/request_detail.html',context)

def productDetailView(request,id):
    context={
        'object':Product.objects.get(id=id)
    }
    return render(request,'main/product_detail.html',context)


def productListPage(request):
    context = {
        'objects': Product.objects.all()
    }
    return render(request, 'main/product_list.html', context)

empty_string = ''

def is_valid_params(param):
    return param!=empty_string and param is not None

def groupListPage(request):

    groups=Group.objects.all()

    qs=request.GET.get('group_name')
    if is_valid_params(qs):
        groups=groups.filter(name__icontains=qs)
    context = {
        'objects': groups
    }
    return render(request,'main/groups.html',context)

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
