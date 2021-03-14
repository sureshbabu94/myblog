from django.shortcuts import render, Http404, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from blog.models import *
from django.contrib import messages
from blog.forms import *
import git
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.


"""
''' Update Server'''
@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("sureshbabu94.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
"""



''' Change password Functionality '''

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


''' Sign Up Functionality '''

def signupform(request):

    #form=UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                #messages.SUCCESS('Logged in Successfully')
                print('Created account and redirecting')
                return redirect('/')
            else:
                HttpResponse("Not Authenticated successfully")
                print('unable to authenticate')
        else:
            messages.error(request,'There is some issue in your form')
            print('form is invalid')
            #form=UserCreationForm()
            #return render(request,'signup.html',{'formfields':form})
    else:
        form = UserForm()
    return render(request,'signup.html',{'formfields':form})


''' Logout Functionality '''

def logoutapp(request):
    print("logging out and clearing sessions", request.user.username)

    request.session.clear_expired()
    logout(request)
    #messages.INFO('Logged Out Successfully')
    return redirect('/')


''' Log In Functionality '''

def loginapp(request):
    if request.user.is_authenticated:
        return HttpResponse('you are already logged in')

    else:
        return redirect('/accounts/login/')


''' Private Posts '''

@login_required(login_url='/accounts/login/')
def yourpost(request):
    your_post_list = Dummy.objects.filter(author=request.user).order_by('-created_on')

   

    paginator = Paginator(your_post_list, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'yourpost.html',{'your_post_list':your_post_list,'page_obj': page_obj})



''' Public Posts and Home Page Functionality with no paginator(Not Active)

def postlist(request):
    post_list = Dummy.objects.filter(status=1).order_by('-created_on')

    return render(request, 'index.html',{'post_list':post_list})
''' 
''' Get post using slug field'''

def postdetail(request, slug):
   # detail = get_object_or_404(Dummy, slug=slug)
    try:
        
        detail = Dummy.objects.filter(status=1).filter(slug=slug).order_by('-created_on')
        print("Got post using slug")
        for x in detail:
            slug_obj = x.id
    except Dummy.DoesNotExist:
        raise Http404
    try:
        comments = Comments.objects.filter(post=slug_obj)
    except Comments.DoesNotExist:
        print("No comments")

    return render(request, 'postdetail.html',{'detail':detail, 'comments':comments})


''' Class based Post Creation Form(Not Active) '''
'''
class CreatePost(LoginRequiredMixin,PermissionRequiredMixin, generic.CreateView):
   # Only Authenticated Authors can create Posts in data base
    #LoginRequired
    login_url='/accounts/login/'

    #PermissionRequired
    permission_required = ('blog.add_post',)
    #raise_exception=True

    #Form
    template_name='postform.html'
    success_url='/'
    model=Post
    fields=('title','author','content','status')
'''


''' Function based Create Post(Dummy) Form '''

@login_required(login_url='/accounts/login/')
@permission_required('blog.add_post', raise_exception=True)
def createrpost(request):
    if request.method=='POST':
        form = DummyForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.author=request.user
            obj.save()
            print('Dummy saved sucessfully')
            return redirect('/')

        else:
            return HttpResponse('Form is invalid')
    else:
        form=DummyForm()
    return render(request,'postform.html',{'form':form})

''' Public Posts and Home Page Functionality with paginator(Active) '''


def pagelist(request):
    object_list = Dummy.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 2) # Show 25 contacts per page.
   # comments=Comment.objects.filter(post=object_list).order_by('-created_on')

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'paginator.html',{'page_obj': page_obj})

def about(request):
    return render(request,'about.html',{})

def contact(request):
    return render(request,'contact.html',{})


''' Edit Private Post '''
@login_required(login_url='/accounts/login/')
@permission_required('blog.add_post', raise_exception=True)
def editpost(request, id):
    try:
        post_id = Dummy.objects.filter(author=request.user).get(id=id)
    except Dummy.DoesNotExist:
        return redirect('your_post')
    form = EditDummyForm(request.POST or None, request.FILES or None, instance = post_id)
    if form.is_valid():
        print("uploaded")
        form.save()
        return redirect('your_post')
    return render(request,'editform.html',{'form':form})


''' Delete Private Post '''
@login_required(login_url='/accounts/login/')
@permission_required('blog.add_post', raise_exception=True)
def delete_post(request, id):
    
    try:
        del_obj = Dummy.objects.filter(author=request.user).get(id = id)
    except Dummy.DoesNotExist:
        return redirect('your_post')
    del_obj.delete()
    return redirect('your_post')



@login_required(login_url='/accounts/login/')
def postcomment(request, slug):
    try:
        dummy_id = Dummy.objects.get(slug=slug)
        print("Post Found")
    except Dummy.DoesNotExist:
        print("Post Not Found")
        return redirect('your_post')
    form_id = dummy_id.id
    print("ID of POST is", form_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        obj=form.save(commit=False)
        obj.post=dummy_id
        print("form post id is",obj.post)
        obj.user=request.user
        print("obj.user is", obj.user)
        obj.save()
        print('Comment saved sucessfully')
        return redirect('/')
    
    return render(request,'commentform.html',{'form':form})
