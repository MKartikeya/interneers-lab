from django.contrib import admin
from .models import Product, Category, Brand, Inventory, Review
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Inventory)
admin.site.register(Review)

