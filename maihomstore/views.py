from django.shortcuts import render
from .models import Catigories,Product

# Create your views here.

def mainpage(request):
    return render(request,'index.html')

def all(request):
    category = Catigories.objects.all()
    product = Product.objects.filter(recommend=True)

    context = {
        'category': category,
        'product' : product
    }
    return render(request,'index.html',{"context" : context})

def category(request):
    return render(request,'index.html')