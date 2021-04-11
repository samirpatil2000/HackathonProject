from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import ProductUploadForm, CreateRequestForm, CreateGroupForm, CommentForm
from .models import RequestForProduct,Product,Group,RequestForJoinGroup,CommentTORequest,RespondToRequest
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

@login_required
def requestListPage(request):
    user = request.user
    account = Account.objects.get(username=user.username)
    try:
        group = account.group
        try:
            request_=RequestForProduct.objects.all().filter(is_submitted=False,group=group)
            context = {
                'objects': request_
            }
            return render(request, 'main/request_list.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, f"{group.name} hase not current active request")
            return redirect('index-page')
    except:
        messages.warning(request, "Please join a group or create instead")
        return redirect('index-page')


@login_required
def requestListPageUSER(request):
    user = request.user
    account = Account.objects.get(username=user.username)
    try:
        group = account.group
        try:
            request_=RequestForProduct.objects.all().filter(is_submitted=False,group=group,user=user)
            context = {
                'objects': request_
            }
            return render(request, 'main/request_list__user.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, f"{group.name} hase not current active request")
            return redirect('index-page')
    except:
        messages.warning(request, "Please join a group or create instead")
        return redirect('index-page')


@login_required
def respond_to_requestDetailView(request,request_id):
    req=RequestForProduct.objects.get(id=request_id)
    responds=RespondToRequest.objects.all().filter(request_for_product=req)
    user=request.user
    context = {
        'objects': responds,
    }
    return render(request,'main/request_list__user_respond.html',context)

@login_required
def requestDetailView(request,id):
    req=RequestForProduct.objects.get(id=id)
    user=request.user
    respond_input = request.GET.get('respond_input')
    if is_valid_params(respond_input):
        current_request = RespondToRequest.objects.create(user=user, request_for_product=req,
                                                          message=respond_input)
        messages.success(request, "Your respond sent successfully ")

    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.request_for_product = req
            user_comment.user=request.user
            user_comment.save()
            return redirect('request-detail', id=id)

    comments = CommentTORequest.objects.filter(request_for_product__id=id)
    context = {
        'object': req,
        'comments': comments,
        'comment_form':comment_form
    }
    return render(request,'main/request_detail.html',context)

def productDetailView(request,id):
    context={
        'object':Product.objects.get(id=id)
    }
    return render(request,'main/product_detail.html',context)


@login_required
def productListPage(request):
    user=request.user
    account = Account.objects.get(username=user.username)
    try:

        group=account.group
        context = {
            'objects': Product.objects.all().filter(group=group)
        }
        return render(request, 'main/product_list.html', context)
    except:
        messages.warning(request, "Please join a group or create instead")
        return redirect('index-page')


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
    try:
        user=request.user
        account=Account.objects.get(username=user.username)
        group=account.group
        productForm=ProductUploadForm()
        if request.method=="POST":
            productForm=ProductUploadForm(request.POST or None)
            if productForm.is_valid():
                prod=productForm.save(commit=False)
                prod.user=user
                prod.group=group
                prod.save()
                return redirect('index-page')
        context={
            'form':productForm
        }
        return render(request,'product/productUploadForm.html',context)
    except:
        messages.warning(request,"Please join a group")
        return redirect('index-page')


@login_required
def create_product_request(request):
    try:
        user=request.user
        account = Account.objects.get(username=user.username)
        group = account.group
        requestForm=CreateRequestForm()
        if request.method=="POST":
            requestForm=CreateRequestForm(request.POST or None)
            if requestForm.is_valid():
                prod_request=requestForm.save(commit=False)
                prod_request.user=user
                prod_request.group = group
                prod_request.save()
                return redirect('index-page')
        context={
            'form':requestForm
        }
        return render(request,'product/createRequestForm.html',context)
    except:
        messages.warning(request,"Please join a group")
        return redirect('index-page')

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
            try:
                RequestForJoinGroup.objects.get(user=user).delete()
            except:
                pass
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
        object=RequestForJoinGroup.objects.get(user=user,is_accepted=False,is_cancelled=False)
        context['group']=object.group
        return render(request,'main/group_request.html',context)
    except ObjectDoesNotExist:
        messages.warning(request, f"No request ..!")
        return redirect('index-page')

@login_required
def cancel_group_joining_request(request):
    user = request.user
    try:
        joining_request=RequestForJoinGroup.objects.get(user=user,is_accepted=False,is_cancelled=False)
        joining_request.is_cancelled=True
        joining_request.save()
        messages.success(request, f"Delete request successfully")
        return redirect('index-page')
    except ObjectDoesNotExist:
        messages.warning(request, f"No request ..!")
        return redirect('index-page')

@login_required
def request_list_for_joining_group(request):
    user=request.user
    current_user=Account.objects.get(username=user.username)
    # try:
    user_group=current_user.group
    try:
        if user in user_group.admins.all():
            context = {
                'group': user_group,
            }
            try:
                joining_requests=RequestForJoinGroup.objects.filter(group=user_group,is_accepted=False,is_cancelled=False)
                context['requests']=joining_requests
            except:
                messages.warning(request,f'There is no any joining request')
            return render(request,'main/group_admin.html',context)
        else:
            context={'group':user_group,'message':"You are not admin"}
        return render(request, 'main/group_admin.html', context)
    except:
        messages.warning(request, f"You Don't have any group")
        return redirect('index-page')



#TODO Some validation required over here
@login_required
def accept_request_for_joining_group(request,username):
    requested_user=Account.objects.get(username=username)
    joining_request=RequestForJoinGroup.objects.get(user=requested_user,is_accepted=False)
    requested_user.group=joining_request.group
    requested_user.save()
    joining_request.is_accepted=True
    joining_request.save()
    messages.success(request,f'{request.user.username } add to group')
    return redirect('request_list_for_joining_group')

@login_required
def cancel_group_joining_request_by_admin(request,username):
    requested_user = Account.objects.get(username=username)
    joining_request = RequestForJoinGroup.objects.get(user=requested_user, is_accepted=False)
    joining_request.is_cancelled=True
    joining_request.save()
    messages.success(request, f"Delete request successfully")
    return redirect('request_list_for_joining_group')

@login_required
def respondToRequest(request,request_id):
    user=request.user
    respond_input=request.GET.get('respond_input')
    if is_valid_params(respond_input):
        current_request=RespondToRequest.objects.create(user=user,request_for_product__id=request_id,message=respond_input)
        messages.success(request,"Your respond sent successfully ")
        # return redirect('respond-to-request',request_id)

        return render(request,'main/request_detail.html')



