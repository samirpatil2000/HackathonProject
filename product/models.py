from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
# Create your models here.

user=settings.AUTH_USER_MODEL

class Category(models.Model):

    name=models.CharField(default="Hammers",max_length=100)

    def __str__(self):
        return str(self.name)


class Product(models.Model):

    user=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.CharField(default="Hammer",max_length=20)
    desc=models.TextField(default="This is the hammer")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    is_borrowed=models.BooleanField(default=False)
    is_on_rent=models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)+str(self.user.name)


class RequestForProduct(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product_name = models.CharField(default="Hammer", max_length=20)
    product_desc = models.TextField(default="This is the hammer")
    request_in_brief=models.TextField(default="I need a hammer for something")
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    is_urgent= models.BooleanField(default=False)
    needed_by=models.DateTimeField(blank=True,null=True)
    return_date=models.DateTimeField(blank=True,null=True)
    is_submitted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)+str(self.product_name)



