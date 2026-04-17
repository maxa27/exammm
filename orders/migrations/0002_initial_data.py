from django.db import migrations


def populate(apps, schema_editor):
    OrderStatus = apps.get_model('orders', 'OrderStatus')
    PickupPoint = apps.get_model('orders', 'PickupPoint')
    Group = apps.get_model('auth', 'Group')

    for name in ['Новый', 'В обработке', 'Готов к выдаче', 'Выдан', 'Отменён']:
        OrderStatus.objects.get_or_create(name=name)

    for address in [
        'ул. Ленина, 1',
        'пр. Мира, 45',
        'ул. Советская, 12',
        'ул. Гагарина, 7',
        'пр. Победы, 30',
    ]:
        PickupPoint.objects.get_or_create(address=address)

    for name in ['Менеджеры', 'Клиенты']:
        Group.objects.get_or_create(name=name)


def depopulate(apps, schema_editor):
    OrderStatus = apps.get_model('orders', 'OrderStatus')
    PickupPoint = apps.get_model('orders', 'PickupPoint')
    OrderStatus.objects.all().delete()
    PickupPoint.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(populate, depopulate),
    ]
