from django.urls import path
from .views import home_page, create_post, post_detail, search_users

urlpatterns = [
    path('', home_page, name='home'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path("search/", search_users, name="search_users"),
]