"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views
#from blog.views import signupform

urlpatterns = [
    path("update_server/", views.update, name="update"),
    path('admin/', admin.site.urls),
    path('',views.postlist, name='home'),
    path('signup/', views.signupform, name='signupform'),
    path('logoutapp/', views.logoutapp, name='logoutapp'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('change_password/', views.change_password, name='change_password'),
    path('loginapp/',views.loginapp,name='loginapp'),
    #public post
    path('postlist/', views.postlist, name='postlist'),
    #private post
    path('yourpost/',views.yourpost, name='your_post'),
    #path('createpost/',views.CreatePost.as_view(), name='createpost'),
    path('createpost/',views.createrpost,name='createpost'),
    

]
