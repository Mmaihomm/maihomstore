from django.shortcuts import render,get_object_or_404
from .models import Catigories,Product,ProductImage
from django.db.models import Q
from django.core.mail import send_mail
from .forms import ContactForm
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def mainpage(request):
    return render(request,'index.html')

def all(request):
    category = Catigories.objects.all()
    product = Product.objects.filter(recommend=True,catigorie__is_active=True)
    categoryid = Catigories.objects.all()

    searchcommit = request.GET.get('search')
    if searchcommit:
        product=product.filter(Q(name__icontains=searchcommit))

    products=[]
    for x in product:
        products.append({
            'pk':x.catigorie.id,
            'id': x.id,
            'name' : x.name,
            'productdetail' : x.productdetail,
            'image' : x.image,
            'price' : x.price
        })
    
    context = {
        'category': category,
        'product' : products,
        'categoryid' : categoryid,
        'searchcommit' : searchcommit
    }
    return render(request,'index.html',{"context" : context})

def Category(request,pk):
    if pk == 1:
        category = Catigories.objects.all()
        product = Product.objects.filter(catigorie__in=category,catigorie__is_active=True)
        category = Catigories.objects.get(pk=pk)
    else:  
        category = Catigories.objects.get(pk=pk)
        product = Product.objects.filter(catigorie=category,catigorie__is_active=True)
    categoryid = Catigories.objects.all()

    searchcommit = request.GET.get('search')
    if searchcommit:
        product=product.filter(Q(name__icontains=searchcommit))


    # sort
    sort = request.GET.get('sort','asc')
    if sort == 'desc':
        product = product.order_by('-price')
    else:
       product = product.order_by('price')

    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    

    context = {
        'product' : product,
        'category' : category, 
        'categoryid' : categoryid,
        'searchcommit' :searchcommit
    }
    return render(request,'categorydetail.html',{"context" : context})

def Productdetails(request,pk,product):
    category = Catigories.objects.get(pk=pk)
    product = Product.objects.get(pk=product)
    productrecommend = Product.objects.filter(recommend=True,catigorie__is_active=True)
    categoryid = Catigories.objects.all()

    post = get_object_or_404(Product,pk=pk)
    photos = ProductImage.objects.filter(product=product)
 
    productrecommends = []
    for x in productrecommend:
        productrecommends.append({
            'pk':x.catigorie.id,
            'id': x.id,
            'name' : x.name,
            'productdetail' : x.productdetail,
            'image' : x.image,
            'price' : x.price,
        })
    
    context = {
        'product' : product,
        'category' : category,
        'categoryid' : categoryid,
        'productrecommend' : productrecommends,
        'photos' : photos
    }
    return render(request,'productdetail.html',{"context" : context})


def contact(request):
    categoryid = Catigories.objects.all()
    if request.method == 'POST':
        token = request.POST.get('g-recaptcha-response')
        secret = requests.post('https://www.google.com/recaptcha/api/siteverify', {
                               'secret': '6Ld1_DcbAAAAALbSH_1fA8gZ7fqjHvznCUANLLLJ', 'response': token})
        form = ContactForm(request.POST)
        print(secret.json()['success'])
        if secret.json()['success']:
            if form.is_valid():
                form.save()
    form = ContactForm()
    context = {
        'form':form,
        'categoryid' : categoryid
        }
    return render(request,'contact.html',{'context' : context})



