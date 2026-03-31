from django.urls import path
from .views import HabitUserView, HabitToggleStatusView, HabitDeleteView

urlpatterns = [
    path('habits-user/', HabitUserView.as_view(), name='habits-user'),
    path('habits-user/<int:pk>/toggle/', HabitToggleStatusView.as_view(), name='habit-toggle'),
    path('habits-user/<int:pk>/habit-delete', HabitDeleteView.as_view(), name='habit-delete'),
]
