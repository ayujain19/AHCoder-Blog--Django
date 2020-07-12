from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# HTML Pages.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def log(request):
    return render(request, 'home/log.html')
def reg(request):
    return render(request, 'home/reg.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10:
            messages.error(request, 'Please fill the form correctly..')
        else:
            contact  = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.error(request, 'Your Messages has been successfully sent.')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none() 
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
         messages.warning(request, "No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)


# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get all Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous input
        if len(username) > 15:
            messages.error(request, 'Your UserName must be under 15 characters')
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, 'Username should only contains letters and numbers')
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not Match')
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your AHCoder Account Has Been Successfully Created!!!')
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please Try Again..')
            return redirect('home')

    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')




   