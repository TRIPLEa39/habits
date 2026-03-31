from django.contrib import admin
from .models import Habit, HabitInfo, HabitWeekDay

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name", "description", "user__username")


@admin.register(HabitWeekDay)
class HabitWeekDayAdmin(admin.ModelAdmin):
    list_display = ("habit", "weekday", "weekday_label")
    list_filter = ("weekday", "habit")
    search_fields = ("habit__name",)

    @admin.display(description="Weekday")
    def weekday_label(self, obj):
        return obj.get_weekday_display()


@admin.register(HabitInfo)
class HabitInfoAdmin(admin.ModelAdmin):
    list_display = ("habit", "date", "status")
    list_filter = ("status", "date", "habit")
    search_fields = ("habit__name",)
    filter_horizontal = ("week_days",)
