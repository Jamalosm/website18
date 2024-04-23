# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
'''
admin.site.register(catagory,categoryadmin)
class categoryadmin(admin.ModelAdmin):
    list_display=('name','image','description')
'''
    
admin.site.register(catagory)
admin.site.register(product)
