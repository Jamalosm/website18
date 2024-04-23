from django.http import JsonResponse
from django.shortcuts import render, redirect
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json


# Create your views here.
def home(request):
    products=product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

####################################
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
 ##################################################
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
 

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Alredy in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Add to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
            
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

# ######################
# def add_to_cart(request):
#    if request.headers.get('x-requested-with')=='XMLHttpRequest':
#     if request.user.is_authenticated:
#       data=json.load(request)
#       product_qty=data['product_qty']
#       product_id=data['pid']
#       #print(request.user.id)
#       product_status=product.objects.get(id=product_id)
#       if product_status:
#         if Cart.objects.filter(user=request.user.id,product_id=product_id):
#           return JsonResponse({'status':'Product Already in Cart'}, status=200)
#         else:
#           if product_status.quantity>=product_qty:
#             Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
#             return JsonResponse({'status':'Product Added to Cart'}, status=200)
#           else:
#             return JsonResponse({'status':'Product Stock Not Available'}, status=200)
#     else:
#       return JsonResponse({'status':'Login to Add Cart'}, status=200)
#    else:
#     return JsonResponse({'status':'Invalid Access'}, status=200)
##########################

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")




def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)  # Corrected typo in 'password'
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully')
                return redirect("/")
            else:
                messages.error(request, 'Invalid Username or Password')  # Corrected typo in 'Username'
                return redirect("/login")
        return render(request, "shop/login.html")

# def login_page(request):
#     if request.user.is_authenticated:
#         return redirect("/")
#     else:
#         if request.method=='POST':
#             name=request.POST.get('username')
#             pwd=request.POST.get('password')
#             user=authenticate(request,username=name,password=pwd)
#             if user is not None:
#                 login(request,user)
#                 messages.success(request,'Logged in Successfully')
#                 return redirect("/")
#             else:
#                 messages.error(request,'Invalid User Name or Password')
#                 return redirect("/login")
#         return render(request,"shop/login.html")


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success You Can Login Now...!")
            return redirect('/login')
    return render(request, "shop/register.html", {"form": form})



def collections(request):
    Catagory=catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"Catagory":Catagory})
def collectionsview(request,name):
    if(catagory.objects.filter(name=name,status=0)):
        products=product.objects.filter(catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"catagory_name":name})
    else:
        messages.warning(request,"No Sush Catagory Found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            Products=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_detail.html",{"Products":Products})
        else:
            messages.warning(request,"No Sush Product Found")
            return redirect('collections')
    else:
        messages.warning(request,"No Sush Catagory Found")
        return redirect('collections')

