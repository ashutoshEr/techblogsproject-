from django.shortcuts import render, HttpResponse, redirect
from home.models import contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.models import User

# html pages
def home(request):
    top_three_post = Post.objects.all().order_by('views').reverse()[0:3]
    context = {'top_three':top_three_post}
    return render(request, 'home/homepage.html', context)


def about(request):

    #messages.success(request, 'this is about us.')
   
    return render(request,'home/about.html')
   
    

def contacts(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<1:
            messages.error(request, "please fill form properly")
        else:    
            contact1 = contact(name=name, email=email, phone=phone, content=content)
            contact1.save()
            messages.success(request, "Your message has been sent successfully")

    return render(request, 'home/contact.html') 

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.obejcts.none()
    else:
        allPoststitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)    
        allPosts = allPoststitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "please search properly")
    params = {'allposts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)
# authentication apis
def Signup(request):
    if request.method == 'POST':
        #get the parameters
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters" )
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "username must contain letters and numbers only")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "please type same password")
            return redirect('home')    
        #create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, 'your account has been successfully created')
        return redirect('home')
    else:
        return render(request,'home/signup.html')

def Login(request):
    if request.method == 'POST':
        #get the parameters
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'suceesfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'invailid credentials, please try again')
            return redirect('home')
        
       
    return render(request,'home/login.html')

def Logout(request):
    logout(request)
    messages.success(request,' you have successfully logged out')
    return redirect('home')
     
    