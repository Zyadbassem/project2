from django.shortcuts import render
from .models import user
# Create your views here.

def sign(request):
    return render(request, "sign.html")