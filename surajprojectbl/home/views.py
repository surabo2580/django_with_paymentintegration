from django.shortcuts import render, HttpResponse,redirect
from home import views
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from blog.models import Post
from django.contrib.auth.models import User
import random

# HTML pages
def home (request):
    #num1 = random.randrange(1,30)
    #num2 = random.randrange(1,50)
    #global str_num,str_num1,str_add
    #str_num1 = str(num1)
    #str_num1 = str(num2)
    #str_num = (f"{num1} + {num2}")
    #str_add = str(num1) + str(num2)
    #if(str_num==str_add):

    num = random.randrange(1, 50)
    global str_num
    str_num = str(num)

    return render(request, 'home/home.html', {'cap': str_num})

    #return render(request,'home/home.html',{'cap':str_num})

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 2:
            messages.error(request,'please fill up the form correctly')
        else:

            contact = Contact(name=name, email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"your form has been submitted successfuly")


    return render(request,'home/contact.html',)

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allposts = Post.objects.none()
    else:
        allpostscontent = Post.objects.filter(content__icontains=query)
        allpostsheadline = Post.objects.filter(headline__icontains=query)
        allposts = allpostscontent.union(allpostsheadline)


    if allposts.count == 0:
        messages.warning(request,'no serach results')
    params = {'allposts':allposts,'query':query}

    return render(request,'home/search.html',params)

# authentication APIS

def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        if username.isalpha():
            messages.error(request,"username can't only contains alphabet")
            return redirect('home')
        if username.isnumeric():
            messages.error(request,"username can't only contain numeric value")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exists")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request,"email already exists")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, " Your accounts has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        captcha = request.POST.get('cap')
        user = authenticate(username=username,password=password)
        if user is not None:
            if str_num == captcha:
                login(request,user)
                messages.success(request,'successfully logged in')
                return redirect('home')
        else:
            messages.error(request,'invalid credentials')
            return redirect('home')
    messages.error(request, 'invalidcaptcha')
    return redirect('home')


def handlelogout(request):
    logout(request)
    messages.success(request,'you have successfully logged out')
    return redirect('home')
