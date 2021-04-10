from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index-page'),
    path('upload-products/',views.uploadProduct,name='upload-products'),
    path('create-product-request/',views.create_product_request,name='create-product-request'),
 ]