from django.contrib import admin
from products.models import Category, Product, Manufacturer, Supplier, Unit


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'supplier']
    list_filter = ['category', 'supplier']
    search_fields = ['name', 'description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    ...


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    ...


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    ...
