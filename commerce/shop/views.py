from django.shortcuts import render, HttpResponse, redirect
from .models import user, item
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout as django_logout
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
        request.session['username'] = username
        return redirect("home")
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

def home(request):
    if 'username' in request.session:
        allItems = item.objects.all()
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': allItems})
    else:
        return redirect('sign')
    
def logout(request):
    django_logout(request)
    request.session.flush()
    return redirect('sign')

def addItems(request):
    #check if user is logged in 
    if 'username' in request.session:
        #if user sends the form
        if request.method == 'POST':
            #get item info
            item_Title = request.POST.get('item_name')
            item_Price = request.POST.get('item_price')
            item_Image = request.POST.get('item_image')
            #check info
            if not item_Image or not item_Price or item_Price < 1 or not item_Title:
                return render(request, 'shop/adder.html', {'username': request.session['username'], 'error': 'Invalid input'})
            #create a new item and saving it
            newItem = item(itemName=item_Title, itemprice=item_Price, itemImage=item_Image)
            newItem.save()
            #redirecting to home page
            return redirect('home')
        #if the user access the page with get
        return render(request, 'shop/adder.html')
    #if the user is not logged in 
    return redirect('sign')