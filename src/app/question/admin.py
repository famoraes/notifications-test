from django.contrib import admin

from .models import Question


@admin.register(Question)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'content'
    )
