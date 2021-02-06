from django.shortcuts import render, redirect
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
# Create your views here.


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



''' Public Posts and Home Page Functionality '''

def postlist(request):
    post_list = Dummy.objects.filter(status=1).order_by('-created_on')
    
    return render(request, 'index.html',{'post_list':post_list})


''' Class based Post Creation Form(Not Active) '''

class CreatePost(LoginRequiredMixin,PermissionRequiredMixin, generic.CreateView):
    '''Only Authenticated Authors can create Posts in data base'''
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



''' Function based Create Post(Dummy) Form '''

@login_required(login_url='/accounts/login/')
@permission_required('blog.add_post', raise_exception=True)
def createrpost(request):
    if request.method=='POST':
        form = DummyForm(request.POST)
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