from django.contrib import admin
from . models import Product, Address, OrderItem, Order, Payment, ColorVariation, SizeVariation

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
