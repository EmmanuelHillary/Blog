from django.urls import path
from .views import post_list, post_detail, post_create, login_user, logout_user, register_user, edit_profile,\
    like_post, edit_post, delete_photo, delete_post, favourite_post, favourite_post_list


app_name = 'post'

urlpatterns = [
    path('', post_list, name='list'),
    path('create-post/', post_create, name='create'),
    path('<int:pk>/<slug:slug>/', post_detail, name='detail'),
    path('<int:pk>/', edit_post, name='edit'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('like/', like_post, name='like_post'),
    path('photo-delete/<int:pk>/', delete_photo, name='photo_delete'),
    path('post-delete/<int:pk>/', delete_post, name='delete'),
    path('favourite-post/<int:pk>/', favourite_post, name='favourite_post'),
    path('favourite-posts/', favourite_post_list, name='favourite_post_list'),
]

