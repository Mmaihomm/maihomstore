from django.shortcuts import render,get_object_or_404,redirect
from .models import Catigories,Product,ProductImage
from django.db.models import Q
from django.core.mail import send_mail
from .forms import ContactForm
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

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

    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

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
        'searchcommit' : searchcommit,
        'recommend' : product
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

    paginator = Paginator(product, 8)
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
        'searchcommit' :searchcommit,
        'pk':pk
    }
    return render(request,'categorydetail.html',{"context" : context})


def Productdetails(request,pk,product):
    category = Catigories.objects.get(pk=pk)
    product = Product.objects.get(pk=product)
    productrecommend = Product.objects.filter(recommend=True,catigorie__is_active=True)
    categoryid = Catigories.objects.all()

    post = get_object_or_404(Product,pk=pk)
    photos = ProductImage.objects.filter(product=product)

    paginator = Paginator(productrecommend, 4)
    page = request.GET.get('page')
    try:
        productrecommend = paginator.page(page)
    except PageNotAnInteger:
        productrecommend = paginator.page(1)
    except EmptyPage:
        productrecommend = paginator.page(paginator.num_pages)

 
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
        'photos' : photos,
        'recommend' : productrecommend
    }
    return render(request,'productdetail.html',{"context" : context})


def contact(request):
    categoryid = Catigories.objects.all()
    if request.method == 'POST':
        token = request.POST.get('g-recaptcha-response')
        secret = requests.post('https://www.google.com/recaptcha/api/siteverify', {
                               'secret': '6Ld1_DcbAAAAALbSH_1fA8gZ7fqjHvznCUANLLLJ', 'response': token})
        print(secret.json()['success'])
        if secret.json()['success']:
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request,messages.SUCCESS,'Message Send','success')
            else:
                messages.add_message(request,messages.ERROR,'Please fill the form','danger')
    form = ContactForm()
    context = {
        'form':form,
        'categoryid' : categoryid
        }
    return render(request,'contact.html',{'context' : context})

def Login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    print(username)
    
    # login
    user = authenticate(username=username,password=password)
    print(user)
    if user is not None :
        login(request,user)
        return redirect('/')
    else:
        messages.info(request,'Username or password is incorrect')
        return redirect('/')

def Logout(request):
    logout(request)
    return redirect('/')

def register(request):
    name=request.POST.get('name')
    lastname=request.POST.get('lastname')
    username=request.POST.get('username')
    password=request.POST.get('password')
    repassword=request.POST.get('repassword')
    email=request.POST.get('email')

    if request.method == 'POST':
        if password==repassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'cannot use username')
                print(name,lastname,username,password,repassword,email)
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'cannot use email')
                print(name,lastname,username,password,repassword,email)
                return redirect('/register')
            else:
                user = User(
                first_name=name,
                last_name=lastname,
                username=username,
                email=email
                )
                user.set_password(password)

                user.save()
                return redirect('/')
        else:
            messages.info(request,'cannot use post')
            return redirect('/register')

    return render(request,'register.html')