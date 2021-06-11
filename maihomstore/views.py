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

def Category(request,name):
    # category = Catigories.objects.get()
    product = Product.objects.filter(catigorie=name)
    return render(request,'categorydetail.html',{"product" : product})