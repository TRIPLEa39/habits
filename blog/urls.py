from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUserView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new', PostCreateView.as_view(), name='post-form'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<str:username>/', PostUserView.as_view(), name='user-posts'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]