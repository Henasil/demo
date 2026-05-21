from django.contrib import admin

from .models import Application, Course, CourseReview, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'user')
    search_fields = ('full_name', 'phone', 'email', 'user__username')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_type', 'duration_hours')
    list_filter = ('course_type',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'start_date', 'start_time', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'start_date')
    search_fields = ('user__username', 'user__profile__full_name', 'course__title')


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'rating', 'created_at')
    list_filter = ('rating',)
