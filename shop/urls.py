from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('cart/', views.cart_page, name='cart'),
    path('collcetions/', views.collections, name='collections'),
    path('collcetions/<str:name>/', views.collectionsview, name='collections'),
    path('collcetions/<str:cname>/<str:pname>', views.product_details, name='product_details'),
    path('addtocart/',views.add_to_cart,name="addtocart"),
    # Add more paths as needed
]
