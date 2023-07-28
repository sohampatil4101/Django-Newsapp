from django.shortcuts import render, redirect, HttpResponse
from Newsapp.models import *
import requests
import random


# api related imports
from django.http import JsonResponse
from django.contrib.auth.models import User
from .serializers import BlogSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status

# mail imports

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import ssl
from email.mime.text import MIMEText




# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
        
    context = {'mail': False, 'pass':False}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        if (len(password) < 5 ):
            context={'pass':True,'mssg':"Password is not strong, should be atleast 5 characters !!", 'mail': False}
            return render(request, 'register.html', context)

        # elif (len(password) < 5 ):
        #     context={'pass':True,'mssg':"Password is not strong, should be atleast 5 characters !!", 'mail': False}
        #     return render(request, 'register.html', context)


        elif ( Appuser.objects.filter(email=email).exists() ):
            context={'mail':True,'mssg':"Email exists!!", 'pass': False}
            return render(request, 'register.html', context)
    



        else:
            ins = Appuser(email = email, password = password)
            ins.save()
            context = {'success': True}
            return render(request, 'register.html', context)


    return render(request, 'register.html')

def login(request):
    context = {'success': False}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        request.session['email'] = email
        print("SOham is greatest", email)

        if (Appuser.objects.filter(email=email, password = password).exists()):
            context = {'email': request.session.get('email')}
            return redirect('newscategories/General',context)


        else:
            context= {'success':True}
            return render(request, 'login.html', context)



    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect('/')

def newshome(request):
    context = {'email': request.session.get('email')}
    return render(request, 'newshome.html', context)

def newscategories(request, category):
    country = "in"
    lan = "en"
    try:
        # url = f"https://newsapi.org/v2/everything?q={category}&from=2023-06-27&sortBy=publishedAt&apiKey=f540fbdbad6f4dda90b31f1c3b6c39f3"
        # url = f"https://newsapi.org/v2/everything?q={category}&from=2023-06-27&sortBy=publishedAt&apiKey=00955dc54af34773bfb30008b3d468de"

        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&language={lan}&apiKey=f540fbdbad6f4dda90b31f1c3b6c39f3"

        newdata = requests.get(url).json()

        articlies = newdata['articles']
        title = []
        desc = []
        img = []
        author = []
        publish = []
        link = []

        for i in range(len(articlies)):
            f = articlies[i]
            title.append(f['title'])
            desc.append(f['description'])
            img.append(f['urlToImage'])
            author.append(f['author'])
            publish.append(f['publishedAt'])
            link.append(f['url'])
        
        mylist = zip(title, desc, img, link)
        context = {'mylist': mylist, 'data': newdata}
        return render(request, 'newscategories.html', context)
    except:
        # print(link)
        print("limit crossed")
        return render(request, 'newscategories.html')

def forgetpassword(request):
    context = {'success': False}
    if request.method == "POST":
        email = request.POST['email']
        data = Appuser.objects.filter(email = email)
        if(data):            
            request.session['otpmail'] = email
            context = {'success': False}
            generateotp(request)
            return redirect('/otpverification', context)
        else:
            context = {'success': True}
            return render(request, 'forgetpassword.html', context)



    return render(request, 'forgetpassword.html')

def generateotp(request):
    global otp
    otp = random.randint(1000,9999) 
    print(otp)
    email = request.session.get('otpmail')
    
    # mail sending
    
    #email from here 
    smtp_server = "smtp.gmail.com"
    port = 587 
    sender_email="patilsoham390@gmail.com"
    receiver_email= email
    password='wlgfzpvqteobtfnq'

    msg = MIMEMultipart()
    msg["Subject"] = "text file sent"
    msg["From"] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg.attach(MIMEText(str(otp)))
    print("Mssg is here: ",email, otp)
    
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # check connection
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # check connection
        server.login(sender_email, password)

        # Send email here
        server.sendmail(sender_email, receiver_email, msg.as_string())

    except Exception as e:
        # Print any error messages to stdout
        print("sarvesr")
        print(e)

    

    return redirect('/otpverification')

def otpverification(request):
    context = {'otp': False, 'email': request.session.get('otpmail')}
    # otp = random.randint(1000,9999)
    print(otp)
    if request.method == "POST":
        getotp = request.POST['otp']
        print(getotp, otp)
        print(type(getotp), type(otp))

        if (otp == int(getotp)):
            print(type(getotp), type(otp))
            print("got") 
            context = {'otp': False}
            return redirect('/changepassword', context)
          
        else:
            print("wrong otp") 
            context = {'otp': True, 'email': request.session.get('otpmail')}
            # return redirect('/otpverification', context)
            return render(request, 'otpverification.html', context)

    return render(request, 'otpverification.html', context)


def changepassword(request): 
    if request.method == "POST":
        newpassword = request.POST['password']

        Appuser_instance = Appuser.objects.get(email=request.session.get('otpmail'))
        Appuser_instance.password = newpassword
        Appuser_instance.save()
        print("done")
        return redirect('/')
        
    context = {'email': request.session.get('otpmail')}
    return render(request, 'changepassword.html', context)


def profile(request):
    data = Blog.objects.filter(email = request.session.get('email'))
    context = {'data': data, 'email': request.session.get('email')}
    return render(request, 'profile.html', context)

def viewblog(request, key, email):
    data = Blog.objects.filter(key = key, email = email)
    context = {'data': data}
    return render(request, 'viewblog.html', context)

def deleteblog(request, key, email):
    data = Blog.objects.get(key = key, email = email)
    data.delete()
    return redirect('/profile')

def createblog(request):
    context = {'success': False}
    if request.method == "POST":
        key = Blog.objects.all()
        for i in key:
            lastkey = i.key
        print(lastkey)
        key = lastkey + 1
        print("New key is: ",key)
        title = request.POST['title']
        content = request.POST['content']
        print(key, request.session.get('email'), title, content)
        data = Blog(key = key, email = request.session.get('email'), title = title, content = content)
        data.save()
        context = {'success': True}
        return render(request, 'createblog.html', context)
    
    return render(request, 'createblog.html', context)

def updateblog(request, key):
    data = Blog.objects.filter(key = key, email = request.session.get('email'))
    context = {'data': data}
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        blog_instance = Blog.objects.get(key=key, email=request.session.get('email'))
        blog_instance.title = title
        blog_instance.content = content
        blog_instance.save()

        email = request.session.get('email')
        return redirect(f'/viewblog/{key}/{email}')
    
    return render(request, 'updateblog.html', context)

# REACT_APP_API_KEY = "f540fbdbad6f4dda90b31f1c3b6c39f3" 
# REACT_APP_API_KEY = "00955dc54af34773bfb30008b3d468de"




# api requests functions 

def blogview(request):
    emp = Blog.objects.all()
    so = BlogSerializer(emp, many=True)
    return JsonResponse(so.data, safe=False)





@csrf_exempt
def blogkeyview(request, key):

    try:
        blog = Blog.objects.get(key=key)
    
    except Blog.DoesNotExist:
        return HttpResponse(status=404)

    # delete endpoint
    if request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status= 202)

    # read endpoint
    elif request.method == 'GET':
        serializer = BlogSerializer(blog)
        return JsonResponse(serializer.data, safe=False)

    # update endpoint
    elif request.method == 'PUT':
        jsonData = JSONParser().parse(request)
        serializer = BlogSerializer(blog, data= jsonData)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data , safe=False)
        
        else:
            return JsonResponse(serializer.errors , safe=False)
        



@csrf_exempt
def createblog(request):
    if request.method == 'GET':
        emp = Blog.objects.all()
        so = BlogSerializer(emp, many=True)
        return JsonResponse(so.data, safe=False)
    # create endpoint
    elif request.method == 'POST':
        jsonData = JSONParser().parse(request)
        serializer = BlogSerializer(data= jsonData)
        if serializer.is_valid():
            employee_instance = serializer.save()  # Save the instance and get the saved object
            return JsonResponse(serializer.data, safe=False)
        
        else:
            return JsonResponse(serializer.errors , safe=False)
        