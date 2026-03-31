from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="habits"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("habits-user")
    
class HabitWeekDay(models.Model):
    class WeekDay(models.IntegerChoices):
        MON = 0, 'Monday'
        TUE = 1, 'Tuesday'
        WED = 2, 'Wednesday'
        THU = 3, 'Thursday'
        FRI = 4, 'Friday'
        SAT = 5, 'Saturday'
        SUN = 6, 'Sunday'
    
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="week_days")
    weekday = models.PositiveSmallIntegerField(choices=WeekDay.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'weekday'], name='unique_habit_weekday')
        ]
    
    def __str__(self):
        return f"{self.habit.name} - {self.get_weekday_display()}"


class HabitInfo(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="infos"
    )
    date = models.DateTimeField(default=timezone.localdate)
    status = models.BooleanField(default=False)
    week_days = models.ManyToManyField(
        HabitWeekDay,
        blank=True, 
        related_name="infos"
    )

    def __str__(self):
        return f"{self.habit.name} ({self.date}) - {'Done' if self.status else 'Not done'}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["habit", "date"], name="unique_habit_date_info")
        ]
