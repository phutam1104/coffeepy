from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def home(request):
    if request.user.is_authenticated:
         customer = request.user
         order,created=Order.objects.get_or_create(customer=customer,complete=False)
         items=order.orderdetails_set.all()
         cartItems=order.get_cart_items
         user_not_login="hidden"
         user_login='show'
    else:
         items=[]
         order={'get_cart_items':0,'get_order_total':0}
         cartItems=order['get_cart_items']
         user_not_login="hidden"
         user_login='show'
    products=Product.objects.all()
    context={'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    # template = loader.get_template('app/index.html')
    # return HttpResponse(template.render(),context)
    return render(request, 'app/index.html',context)

def cart(request):
    if request.user.is_authenticated:
         customer = request.user
         order,created=Order.objects.get_or_create(customer=customer,complete=False)
         items=order.orderdetails_set.all()
         cartItems=order.get_cart_items

    else:
         items=[]
         order={'get_cart_items':0,'get_order_total':0}
         cartItems=order['get_cart_items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
         customer = request.user
         order,created=Order.objects.get_or_create(customer=customer,complete=False)
         items=order.orderdetails_set.all()
         cartItems=order.get_cart_items
         
    else:
         items=[]
         order={'get_cart_items':0,'get_order_total':0}
         cartItems=order['get_cart_items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'app/checkout.html',context)
def updateItems(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    customer=request.user
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderDetails,created=OrderDetails.objects.get_or_create(order=order,product=product)
    if action=='add':
         orderDetails.quantity +=1
    elif action=='remove':
         orderDetails.quantity -=1
    orderDetails.save()
    if orderDetails.quantity<=0:
        orderDetails.delete()
    return JsonResponse('added',safe=False)
def register(request):
     form=CreateUserForm()
     if request.method =='POST': 
          form = CreateUserForm(request.POST)
     if form.is_valid():
          form.save()
          return redirect('login')
     context={'form':form}

     return render(request, 'app/register.html',context)
def loginPage(request):
     if request.user.is_authenticated:
          return redirect('home')
     if request.method =='POST': 
          username=request.POST.get('username')
          password=request.POST.get('password')
          user=authenticate(request,username=username,password=password)
          if user is not None:
               login(request,user)
               return redirect('home')
          else:
               messages.info(request,'user or password not correct')
     context={}
     return render(request, 'app/login.html',context)
def logoutPage(request):
     logout(request)
     return redirect('login')
