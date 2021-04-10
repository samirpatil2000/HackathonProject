from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import ProductUploadForm,CreateRequestForm,CreateGroupForm
from .models import RequestForProduct,Product,Group,RequestForJoinGroup
from django.contrib import messages
from account.models import Account
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

@login_required
def createGroup(request):
    user=request.user
    gpForm=CreateGroupForm()
    if(request.method=="POST"):
        gpForm=CreateGroupForm(request.POST or None)
        if gpForm.is_valid():
            gp=gpForm.save(commit=False)
            gp.save()
            gp.admins.add(user)
            current_user_account=Account.objects.get(username=user.username)
            current_user_account.group=gp
            current_user_account.save()
            messages.success(request,f"You successfully created group {gp.name}")
            return redirect('index-page')
    context={'form':gpForm}
    return render(request,'product/create_group.html',context)


@login_required
def sendRequestGroup(request,group_id):
    user = request.user
    group = Group.objects.get(id=group_id)
    try:
        RequestForJoinGroup.objects.create(user=user,group=group)
        messages.success(request,f"You successfully send request to join {group.name}")
        return redirect('index-page')
    except:
        messages.warning(request, f"You can send only request at a time")
        return redirect('index-page')
    # return render(request,'main/groups.html')

@login_required
def view_send_request_to_group(request):
    user=request.user
    context={}
    try:
        object=RequestForJoinGroup.objects.get(user=user)
        context['group']=object.group
        return render(request,'main/group_request.html',context)
    except ObjectDoesNotExist:
        messages.warning(request, f"No request ..!")
        return redirect('index-page')

@login_required
def cancel_group_joining_request(request):
    user = request.user
    try:
        RequestForJoinGroup.objects.get(user=user).delete()
        messages.success(request, f"Delete request successfully")
        return redirect('index-page')
    except ObjectDoesNotExist:
        messages.warning(request, f"No request ..!")
        return redirect('index-page')
