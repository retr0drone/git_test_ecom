from django.contrib import admin
from . models import Product, Address, OrderItem, Order, Payment

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
