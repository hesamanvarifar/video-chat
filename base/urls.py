from django.urls import path
from .views import lobby, room, get_token, create_user, get_member

urlpatterns = [
    path("", lobby),
    path("room/", room),
    path("get_token/", get_token),
    path("create_user/", create_user),
    path("get_member/", get_member),
]
