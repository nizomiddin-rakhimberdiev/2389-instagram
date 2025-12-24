from django.urls import path
from .views import start_chat, chat_detail, login_view, profile_view, logout_view, register_view, inbox

urlpatterns = [
    path('login/', login_view, name='login'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('messages/', inbox, name='messages'),
    path("start/<str:username>/", start_chat, name="start_chat"),
    path("<int:chat_id>/", chat_detail, name="chat_detail"),
]