from django.db.models import Prefetch
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Habit, HabitInfo


class HabitUserView(LoginRequiredMixin, CreateView, ListView):
    model = Habit
    template_name = 'habits/habit_user.html'
    fields = ['name', 'description']
    context_object_name = 'habits'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        today = timezone.localdate()
        today_infos = HabitInfo.objects.filter(date=today).only("habit_id", "status")
        return (
            Habit.objects.filter(user=self.request.user)
            .prefetch_related(Prefetch("infos", queryset=today_infos, to_attr="today_infos"))
            .order_by('-created_at')
        )

class HabitUpdateView(LoginRequiredMixin, UpdateView):
    pass


class HabitToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        today = timezone.localdate()
        info, _ = HabitInfo.objects.get_or_create(habit=habit, date=today)
        info.status = not info.status
        info.save(update_fields=["status"])
        return redirect("habits-user")
    
class HabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        habit = get_object_or_404(Habit, pk=self.kwargs["pk"])
        return self.request.user == habit.user

    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit.delete()
        return redirect("habits-user")
