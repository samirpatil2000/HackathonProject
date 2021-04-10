from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index-page'),
    path('upload-products/',views.uploadProduct,name='upload-products'),
    path('create-product-request/',views.create_product_request,name='create-product-request'),
    path('request-page/',views.requestListPage,name='request-page'),
    path('request/<id>',views.requestDetailView,name="request-detail"),
    path('product/<id>',views.productDetailView,name="product-detail"),
 ]