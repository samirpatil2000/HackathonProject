from django.contrib import admin
from .models import Product,RequestForProduct,Category,Group,GroupAddress,RequestForJoinGroup
# Register your models here.

admin.site.register(Product)
admin.site.register(RequestForProduct)
admin.site.register(Category)

admin.site.register(Group)
admin.site.register(GroupAddress)
admin.site.register(RequestForJoinGroup)