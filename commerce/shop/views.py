from django.shortcuts import render, HttpResponse
from .models import user
import hashlib
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
        if userEntering.hashPassword != password:
            return render(request, 'shop/sign.html', {'error': "wrong password/username"})
        return HttpResponse("works")


    return render(request, 'shop/sign.html')