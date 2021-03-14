from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from uuid import uuid4
#from .models import Dummy

# Create your models here.

from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

    
class Profile(models.Model):
    pass


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
    first_img = models.ImageField(upload_to=path_and_rename) 
    second_img = models.ImageField(upload_to=path_and_rename) 
    third_img = models.ImageField(upload_to=path_and_rename) 
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
