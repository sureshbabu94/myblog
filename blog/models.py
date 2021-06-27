from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from uuid import uuid4
import re
from django.core.exceptions import ValidationError
#from .models import Dummy

# Create your models here.

from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

def validate_mobile(value):
    num=re.search('[+][0-9]{1,3}[6789][0-9]{9}',value)
    if num:
        return value
    else:
        raise ValidationError('Enter valid mobile number starts with country code example: +917XXXXXXX6 ')

def validate_email(value):
    
    if value=='xyz@xyz.com':
        raise ValidationError('Enter valid email id example: xyz@xyz.com ') 
    else:
        return value

class Profile(models.Model):
    bio=models.TextField(max_length=120, blank=True, null=False)
    location=models.CharField(max_length=100,blank=True, null=False)
    first_name = models.CharField(max_length=150, blank=True, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    email = models.EmailField(default='xyz@xyz.com',unique=True,validators=[validate_email])
    mobile= models.CharField(max_length=14, blank=True, null=False,validators=[validate_mobile],help_text="Mobile should start with country code followed by mobile number ex: +918724567890")



def path_and_rename(instance, filename):
   # upload_to = 'images'
    ext = filename.split('.')[-1]
    print(ext)
    # get filename
    filename = '{}.{}'.format(uuid4().hex, ext)
    print(filename)
    #print(instance.user.username)
    return 'Title_{0}/{1}'.format(instance.title, filename)

class Dummy(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, default='empty-slug')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
   # first_img = models.ImageField(upload_to=path_and_rename,blank=True,null=True) 
    #second_img = models.ImageField(upload_to=path_and_rename,blank=True,null=True) 
    #third_img = models.ImageField(upload_to=path_and_rename,blank=True,null=True) 
    status = models.IntegerField(choices=STATUS, default=0, help_text='Publish-will publish your post in Public blog, Draft-will publish your post in your private blog')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.title)
        #this line below save every fields of the model instance
        super(Dummy, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("postdetail", kwargs={"slug": str(self.slug)})


    #def get_absoulte_url(self):

    #objects = models.Manager()


class Comments(models.Model):
    post = models.ForeignKey(Dummy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.user.username
'''
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.user = instance.user
        #this line below save every fields of the model instance
        super(Comment, self).save(*args, **kwargs)
'''
