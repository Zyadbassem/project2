from django.shortcuts import render, HttpResponse, redirect
from .models import User, ItemUpdated, Bid
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
        userEntering = User.objects.filter(username=username).first()
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
        checker = User.objects.filter(username=username).first()
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
        userEntering = User(username=username, hashPassword=make_password(password))
        userEntering.save()
        return redirect('sign')
    return render(request, 'shop/register.html')

def home(request):
    #check if user is logged in
    if 'username' in request.session:
        allItems = ItemUpdated.objects.all()
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': allItems})
    #if user isn't logged in
    else:
        return redirect('sign')
    
def logout(request):
    #clear user info from session
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
            item_type  = request.POST.get('item_type')
            item_description = request.POST.get('item_description')
            #check info
            if not item_Image or not item_Price or not item_Title or not item_description or item_type == '':
                return render(request, 'shop/adder.html', {'username': request.session['username'], 'error': 'Invalid input'})
            #create a new item and saving it
            newItem = ItemUpdated(item_name=item_Title, item_price=item_Price, item_image=item_Image, item_description=item_description, item_type=item_type)
            newItem.save()
            #redirecting to home page
            return redirect('home')
        #if the user access the page with get
        return render(request, 'shop/adder.html', {'username': request.session['username']})
    #if the user is not logged in 
    return redirect('sign')

def itemPage(request, clickedItemTitle):
    #get the clicked item
    clickedItem = ItemUpdated.objects.filter(item_name= clickedItemTitle).first()
    #get user info
    activeUser = User.objects.filter(username=request.session['username']).first()
    if not clickedItem:
        return HttpResponse('404item not found')
    #if the user sends a form 
    if request.method == 'POST':
        #get the new bid the user will enter
        newBid = int(request.POST.get('newBid'))
        if not newBid or newBid < clickedItem.item_price:
            return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username, 'error': 'bid not valid'})
        bidAdder = Bid(buyerId=activeUser, itemId=clickedItem, bidAmount=newBid)
        bidAdder.save()
        clickedItem.item_price = newBid
        clickedItem.save()
        return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username})
    return render(request, 'shop/itemPage.html', {'item': clickedItem, 'username': activeUser.username})
def types(request, typeClicked):
    if 'username' in request.session:
        allItems = ItemUpdated.objects.filter(item_type=typeClicked)
        return render(request, 'shop/home.html', {'username': request.session['username'], 'items': allItems})
    #if user isn't logged in
    else:
        return redirect('sign')
        