from email.message import EmailMessage
# from lib2to3.pgen2.tokenize import generate_tokens
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from userAPI import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from . tokens import generate_token
from django.core.mail import EmailMessage



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
            
        elif User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            
        elif password!=cpassword:
            messages.error(request, "Password mismatch")
            
        elif len(password)<8 or len(password)>16:
            messages.error(request, "Password must be 8-16 character long")
            
        elif len(username)>10:
            messages.error(request, "Username is too large")
            
        elif len(username)<5:
            messages.error(request, "Username is too small")
        
        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your account has been successfully created. we have sent you a confirmation email, please confirm your email in order to activate your account!")
            
            # welcome message
            subject = "Welcome to bytecode velocity - login"
            message = "hello "+myuser.first_name+" \n"+" Thank you for visiting our website \n we also sent you a confirmation email, please confirm your email in order to activate your account! \n\n\n Regards, Jean Claude HIRWA"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email,to_list, fail_silently=True )
            
            
            
            # Email address confirmation email
            current_site = get_current_site(request)
            email_subject = "Confirm your email at Bytecode Velocity - Login"
            message2 = render_to_string("email_confirmation.html"),{
                'name' : myuser.first_name,
                'domain' : current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            }
            email = EmailMessage(email_subject,
                                 message2,
                                 settings.EMAIL_HOST_USER,
                                 myuser.email,
                                 )
            email.fail_silently = True
            email.send()
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
            
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text