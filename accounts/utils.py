def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    if user.is_superuser:
        return 'admin'
    groups = set(user.groups.values_list('name', flat=True))
    if 'Менеджеры' in groups:
        return 'manager'
    if 'Клиенты' in groups:
        return 'client'
    return 'guest'
