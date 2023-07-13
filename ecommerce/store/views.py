from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime


def store(request):
   
    Products = Product.objects.all()
    context ={'Products': Products}
    return render(request, 'store/store.html',context)







def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer , complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
    context ={'items':items, 'order':order}
    return render(request, 'store/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer , complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    context ={'items':items, 'order':order}
    return render(request, 'store/checkout.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action= data['action']

    print('Action: ', action)
    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer , complete = False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity +1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity -1)

    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item was added', safe=False)

import os
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer , complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            print(data)
            
            ShippingAddress.objects.create(
                
                Customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )

        subject = "Order Status from SuGuBuy.com"
        message = "Your Order is successfully completed and you will get the order at your given address..."
        from_email = settings.EMAIL_HOST_USER
        to_email = customer.email
        recipient_list = [to_email]
        
        
        try:
            send_mail(subject, message, from_email, recipient_list)
            print('Email sent')
        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')

            





        



    

    else:
        print('User is not logged in...')
    return JsonResponse('Payment Complete!', safe=False)





def search(request):
    Products = Product.objects.all()
    search_query = request.GET.get('query', '')
    products = Product.objects.filter(name=search_query)
 
    

    context ={'Products': products,'allProducts':Products}
  
    return render(request, 'store/search.html',context)


from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from store.models import Customer


# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        user = request.POST['username']
        passw = request.POST['passw']
        user = authenticate(request, username = user , password = passw)
        print(user)
        if user is not None:        
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials !!!')
            return render(request, 'store/login.html')

        

    else:
        
        return render(request, 'store/login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['userName']
        Email = request.POST['ph']
        passw = request.POST['pass']
        passc = request.POST['conpass']
        
        

        if passw == passc:
            if User.objects.filter(username=name).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email=Email).exists():
                messages.info(request, 'Email ID already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=name,password=passw,email=  Email)
                customer = Customer(user=user, name=name, email=Email)
                customer.save()
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password didnot matched!')
            return redirect('register')

    else:
        return render(request, 'store/register1.html')


