from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
# Create your models here.
from django.urls import reverse
from mptt.models import MPTTModel,TreeForeignKey

from django.utils import timezone
import random
user=settings.AUTH_USER_MODEL



class GroupAddress(models.Model):

    street=models.CharField(max_length=200,blank=True,null=True,default="StreetA")
    locality=models.CharField(max_length=200,blank=True,null=True,default="Locality A")
    #TODO add validators here
    Pincode=models.IntegerField(blank=True,null=True,default=401503)
    Post=models.CharField(blank=True,null=True,max_length=150,default="POST-A")
    District=models.CharField(max_length=200,blank=True,null=True,default="MUMBAI")
    State=models.CharField(max_length=200,blank=True,null=True,default="MAHARASHTRA")



class Group(models.Model):

    name=models.CharField(max_length=50)
    admins= models.ManyToManyField(user, blank=True,related_name="group_admins")
    group_address=models.OneToOneField(GroupAddress,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.name)


class RequestForJoinGroup(models.Model):

    user=models.OneToOneField(user,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_cancelled= models.BooleanField(default=False)




#
#
# class GroupAdmin(models.Model):
#     group=models.OneToOneField(Group,on_delete=models.CASCADE)
#     group_admins=models.ManyToManyField(user,blank=True)
#
#     def __str__(self):
#         return str(self.group.name)






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
    thumbnail=models.ImageField(upload_to='product_images',blank=True,null=True)
    group=models.ForeignKey(Group,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.name)+" "+str(self.user.username)

    def get_product_absolute_url(self):
        return reverse('product-detail',kwargs={'id':self.id})


TIMES=(

    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (7,7),
    (15,15),
)

product_list=['hammer','hpenvy-234 charger','screw driver','drilling machine','machine','mechanical drive']
x=product_list[random.randint(0,len(product_list)-1)]
class RequestForProduct(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product_name = models.CharField(default=x, max_length=50)
    product_desc = models.TextField(default=f"This is the {x}",blank=True,null=True)
    request_in_brief=models.TextField(default=f"I need a {x} for something",blank=True,null=True,)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    is_urgent= models.BooleanField(default=False)
    date_needed_by=models.DateTimeField(default=timezone.now(),blank=True,null=True,help_text="Format 2021-04-11 04:08:08")
    time_needed_by=models.IntegerField(choices=TIMES,blank=True,null=True)
    return_date=models.DateTimeField(default=timezone.now(),blank=True,null=True,help_text="Format 2021-04-11 04:08:08")
    is_submitted=models.BooleanField(default=False)
    group=models.ForeignKey(Group,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return str(self.user)+str(self.product_name)

    def get_request_absolute_url(self):
        return reverse('request-detail',kwargs={'id':self.id})


class RespondToRequest(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    request_for_product = models.OneToOneField(RequestForProduct, on_delete=models.CASCADE)
    message=models.CharField(max_length=200,default="I have this one")


    def __str__(self):
        return f"{self.user.username} {self.request_for_product.product_name}"


class CommentTORequest(MPTTModel):
    request_for_product=models.ForeignKey(RequestForProduct,on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField(default="This is the comment")
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)


    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'comment on {self.request_for_product.product_name}'


