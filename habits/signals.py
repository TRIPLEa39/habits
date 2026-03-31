from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import HabitInfo, HabitWeekDay, Habit

@receiver(post_save, sender=Habit)
def create_habit_info(sender, instance, created, **kwargs):
    """Automatically create a HabitInfo when a new Habit is created."""
    if created:
        HabitInfo.objects.create(habit=instance)

@receiver(m2m_changed, sender=HabitInfo.week_days.through)
def validate_week_days_match_habit(sender, instance, action, pk_set, **kwargs):
    if action != "pre_add" or not pk_set:
        return
    
    invalid = HabitWeekDay.objects.filter(pk__in=pk_set).exclude(habit=instance.habit)
    if invalid.exists():
        raise ValidationError("All schedule days must belong to the same habit as HabitInfo.")
