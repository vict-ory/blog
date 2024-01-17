from django.shortcuts import render, redirect
from account.models import User, Newsletter
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.conf import settings
from django.core.mail import send_mail
from random import randrange


# Create your views here.

def register(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email address already taken')
            return redirect('register')
        
        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Phone number already taken')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')
        
        if pass1 != pass2:
            messages.error(request, 'Password does not match')
            return redirect('register')
        
        

        #send email to user
        subject = 'welcome to DJANGO world'
        message = f'Hi {username}, thank you for registering.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list,fail_silently=False )
        
        user = User.objects.create_user(username,email,pass1)
        user.first_name = first
        user.last_name = last
        user.mobile = mobile
        user.save()

        messages.success(request, 'Done')
        return redirect('home')
        

    return render(request, 'account/register.html')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

        else:
            messages.error(request, 'Invalid user')
            return redirect('login')
        return redirect('home')
    return render(request, 'account/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    get_user = request.user
    user = User.objects.get(mobile=get_user.mobile)
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Done')
            return redirect('profile')
    context = {
        'form':form
    }
    return render(request, 'account/profile.html',context)

def createNewsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        Newsletter.objects.create(email=email)
    return redirect('home')

def sendNewsletter(request):
    if request.method == 'POST':
        receiver = []
        mails = Newsletter.objects.filter(status=True)
        for mail in mails:
            receiver.append(mail.email)

        print(receiver)
        # send email to user
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_from = settings.EMAIL_HOST_USER
        send_mail( subject, message, email_from, receiver,fail_silently=False )
        messages.success(request, 'Sent')
        return redirect('send-newsletter')

    return render(request, 'account/newsletter.html')

def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        user_email = User.objects.get(email=email)
        if user.exists():
            str_code = str(randrange(0,999999))
            code = str_code.zfill(6)
            # send email to user
            subject = 'RESET PASSWORD'
            message = str(code)
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, [user_email.email],fail_silently=False )
            user.update(forget_password_code=code)
            messages.success(request, 'A code has been send to your email')
            return redirect('code',user_email.ref)

        else:
            messages.error(request, 'Email does not exist')
            return redirect('login')

    return render(request, 'account/forget_password.html')

def code(request, ref):
    if request.method == 'POST':
        user = User.objects.get(ref=ref)
        user_code = request.POST.get('code')
        if user_code == user.forget_password_code:
            messages.success(request, 'Correct code')
            return redirect('new-password', user.ref)
        else:
            messages.error(request, 'Incorrect code')
            return redirect('code', ref)

    return render(request, 'account/password_code.html')

def newPassword(request, ref):
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        user = User.objects.get(ref=ref)

        if pass1 == pass2:
            user.set_password(pass1)
            # user.forget_password_code = None
            user.save()
            
            messages.success(request, 'Done')
            return redirect('home')
        else:
            messages.error(request, 'Password mismatch')
            return redirect('new-password', ref)
    return render(request, 'account/new_password.html')