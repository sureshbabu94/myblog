from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, default='empty-slug')
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0, help_text='Publish-will publish post in this blog, Draft-will not publish post in this blog')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.title)
        #this line below save every fields of the model instance
        super(Post, self).save(*args, **kwargs)


    #def get_absoulte_url(self):

    #objects = models.Manager()


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    
class Profile(models.Model):
    pass

class Dummy(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, default='empty-slug')
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
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
