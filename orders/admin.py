from django.contrib import admin
from .models import Order, OrderItem, OrderStatus, PickupPoint


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'status', 'pickup_point', 'order_date']
    list_filter = ['status']
    search_fields = ['order_number', 'customer__username']
    inlines = [OrderItemInline]


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    ...


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    ...
