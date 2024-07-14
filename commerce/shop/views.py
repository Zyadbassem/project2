from django.shortcuts import render, HttpResponse, redirect
from .models import user
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
def sign(request):
    #if user sends a form
    if request.method == 'POST':
        #get username and check it
        username = request.POST.get('username')
        if not username:
            return render(request, 'shop/sign.html', {'error': "please enter username"})
        if len(username) < 4:
           return render(request, 'shop/sign.html', {'error': "username not valid"})
        #get password and check it
        password = request.POST.get('password')
        if not password:
            return render(request, 'shop/sign.html', {'error': "please enter password"})
        if len(password) < 4:
           return render(request, 'shop/sign.html', {'error': "password not valid"})
        #check if username and password are in db
        userEntering = user.objects.filter(username=username).first()
        if not userEntering:
            return render(request, 'shop/sign.html', {'error': "wrong password/username"})
        if not check_password(password, userEntering.hashPassword):
            return render(request, 'shop/sign.html', {'error': "wrong password/username"})
        return HttpResponse("works")
    #if user access via get
    return render(request, 'shop/sign.html')

def register(request):
    if request.method == "POST":
       #get username and check it
        username = request.POST.get('username')
        if not username:
            return render(request, 'shop/register.html', {'error': "please enter username"})
        if len(username) < 4:
           return render(request, 'shop/register.html', {'error': "username not valid"})
        checker = user.objects.filter(username=username).first()
        if checker:
            return render(request, 'shop/register.html', {'error': "user already exists"})
        #get password and check it
        password = request.POST.get('password')
        passwordcon = request.POST.get('passwordCon')
        if not password:
            return render(request, 'shop/register.html', {'error': "please enter password"})
        if len(password) < 4:
           return render(request, 'shop/register.html', {'error': "password not valid"})
        if password != passwordcon:
            return render(request, 'shop/register.html', {'error': "passwords don't match"})
        #add user to db
        userEntering = user(username=username, hashPassword=make_password(password))
        userEntering.save()
        return redirect('sign')
    return render(request, 'shop/register.html')