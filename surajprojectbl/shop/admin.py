from django.contrib import admin
from shop.models import Product,Order,orderUpdate
# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(orderUpdate)
