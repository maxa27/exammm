from .utils import get_user_role


def current_user_role(request):
    return {'current_user_role': get_user_role(request.user)}
