from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderStatus
from .forms import OrderForm, OrderAdminForm, OrderStatusForm, OrderItemCreateFormSet, OrderItemUpdateFormSet
from accounts.utils import get_user_role


@login_required
def order_list(request):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'Доступ запрещён.')
        return redirect('products:product_list')

    if role == 'client':
        orders = Order.objects.filter(customer=request.user).select_related(
            'status', 'pickup_point'
        )
    else:
        orders = Order.objects.select_related('status', 'pickup_point', 'customer')

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'user_role': role,
    })


@login_required
def order_detail(request, pk):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'Доступ запрещён.')
        return redirect('products:product_list')

    order = get_object_or_404(Order, pk=pk)
    if role == 'client' and order.customer != request.user:
        messages.error(request, 'У вас нет доступа к этому заказу.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'user_role': role,
    })


@login_required
def order_create(request):
    role = get_user_role(request.user)
    if role not in ('client', 'admin'):
        messages.error(request, 'У вас нет прав для создания заказов.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemCreateFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            default_status = OrderStatus.objects.filter(name='Новый').first()
            if not default_status:
                default_status = OrderStatus.objects.first()

            order = form.save(commit=False)
            order.customer = request.user
            order.status = default_status
            order.save()

            for item_form in formset:
                cd = item_form.cleaned_data
                if cd and not cd.get('DELETE', False):
                    item = item_form.save(commit=False)
                    item.order = order
                    item.price = item.product.final_price
                    item.save()

            messages.success(request, f'Заказ {order.order_number} успешно создан.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemCreateFormSet()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Создать заказ',
        'user_role': role,
    })


@login_required
def order_update(request, pk):
    role = get_user_role(request.user)
    order = get_object_or_404(Order, pk=pk)

    if role not in ('manager', 'admin'):
        messages.error(request, 'У вас нет прав для редактирования заказов.')
        return redirect('orders:order_list')

    FormClass = OrderAdminForm if role == 'admin' else OrderStatusForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=order)
        formset = OrderItemUpdateFormSet(request.POST, instance=order) if role == 'admin' else None

        form_valid = form.is_valid()
        formset_valid = formset.is_valid() if formset is not None else True

        if form_valid and formset_valid:
            form.save()
            if formset is not None:
                items = formset.save(commit=False)
                for item in items:
                    if not item.pk:
                        item.price = item.product.final_price
                    item.save()
                for item in formset.deleted_objects:
                    item.delete()
            messages.success(request, f'Заказ {order.order_number} обновлён.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = FormClass(instance=order)
        formset = OrderItemUpdateFormSet(instance=order) if role == 'admin' else None

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'order': order,
        'title': 'Редактировать заказ',
        'user_role': role,
    })


@login_required
def order_delete(request, pk):
    role = get_user_role(request.user)
    order = get_object_or_404(Order, pk=pk)

    if role != 'admin':
        messages.error(request, 'У вас нет прав для удаления заказов.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        order_number = order.order_number
        order.delete()
        messages.success(request, f'Заказ {order_number} удалён.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': role,
    })
