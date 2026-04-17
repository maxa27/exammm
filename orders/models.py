from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
        ordering = ['name']

    def __str__(self):
        return self.name


class PickupPoint(models.Model):
    address = models.CharField(max_length=300, unique=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'
        ordering = ['address']

    def __str__(self):
        return self.address


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата доставки')
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент'
    )
    status = models.ForeignKey(
        OrderStatus, on_delete=models.PROTECT, verbose_name='Статус'
    )
    pickup_point = models.ForeignKey(
        PickupPoint, on_delete=models.PROTECT, verbose_name='Пункт выдачи'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            count = Order.objects.filter(
                order_number__startswith=f'ORD-{date_str}'
            ).count()
            self.order_number = f'ORD-{date_str}-{count + 1:04d}'
        super().save(*args, **kwargs)

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        unique_together = [['order', 'product']]

    def __str__(self):
        return f'{self.order.order_number} — {self.product.name}'

    def subtotal(self):
        return self.price * self.quantity
