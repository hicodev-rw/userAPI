from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if User.objects.filter(username=username):
            messages.error(request, "username already exists")
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            
        if password!=cpassword:
            messages.error(request, "Password mismatch")
            
        if len(password)<8 or len(password)>16:
            messages.error(request, "Password must be 8-16 character long")
            
        if len(username)>10:
            messages.error(request, "Username is too large")
            
        if len(username)<5:
            messages.error(request, "Username is too small")
        
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect('signin')

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            firstname = user.first_name
            return render(request, 'index.html', {'name':firstname})
        else:
            messages.error(request, "Bad Confidential!")
            return redirect('home')
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('home')

