from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_point', 'delivery_date']
        widgets = {
            'pickup_point': forms.Select(attrs={'class': 'form-select'}),
            'delivery_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'].required = False
        self.fields['delivery_date'].input_formats = ['%Y-%m-%dT%H:%M']


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_point', 'status', 'delivery_date']
        widgets = {
            'pickup_point': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'delivery_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'].required = False
        self.fields['delivery_date'].input_formats = ['%Y-%m-%dT%H:%M']


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'delivery_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'delivery_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_date'].required = False
        self.fields['delivery_date'].input_formats = ['%Y-%m-%dT%H:%M']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


OrderItemCreateFormSet = formset_factory(OrderItemForm, extra=2, min_num=1, validate_min=True)

OrderItemUpdateFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    min_num=0,
    can_delete=True,
)
