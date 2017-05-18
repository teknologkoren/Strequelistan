from django.contrib import admin

# Register your models here.

from .models import Transaction, Quote, Group, PriceGroup, Product, ProductCategory,PriceLimit, RegisterRequest

admin.site.register(Transaction)
admin.site.register(Quote)
admin.site.register(Group)
admin.site.register(PriceGroup)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(PriceLimit)
admin.site.register(RegisterRequest)