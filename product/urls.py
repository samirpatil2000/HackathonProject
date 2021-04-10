from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index-page'),
    path('upload-products/',views.uploadProduct,name='upload-products'),
    path('create-product-request/',views.create_product_request,name='create-product-request'),
    path('request-page/',views.requestListPage,name='request-page'),
    path('product-page/',views.productListPage,name='product-page'),
    path('request/<id>',views.requestDetailView,name="request-detail"),
    path('product/<id>',views.productDetailView,name="product-detail"),
    path('groups/',views.groupListPage,name='groups'),
    path('create-group/',views.createGroup,name='create-group'),

    #send request
    path('send-joining-request/<group_id>',views.sendRequestGroup,name="send_joining_request"),
    path('view-send-joining-request/',views.view_send_request_to_group,name="view_send_joining_request"),
    path('cancel-joining-request/',views.cancel_group_joining_request,name="cancel_group_joining_request"),

    path('group-joining-request/',views.request_list_for_joining_group,name='request_list_for_joining_group'),
    path('accept-group-joining-request/<str:username>',views.accept_request_for_joining_group,name='accept_request_for_joining_group'),
    path('cancel-group-joining-request/<str:username>',views.cancel_group_joining_request_by_admin,name='cancel_group_joining_request_by_admin'),
 ]


#TODO
# add urls to messages
# group filter with address
# request filter with address
# post filer