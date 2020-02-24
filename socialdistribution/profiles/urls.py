from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.author_profile, name='author-profile'),
    path('posts/', views.current_visible_posts, name='visible-posts'),
    path('<uuid:author_id>/posts/', views.author_posts, name='author-posts'),
]