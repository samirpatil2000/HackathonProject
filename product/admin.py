from django.contrib import admin
from .models import Product,RequestForProduct,Category
# Register your models here.

admin.site.register(Product)
admin.site.register(RequestForProduct)
admin.site.register(Category)