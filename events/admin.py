from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'task', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['user__email', 'task__title', 'event_type']
    readonly_fields = ['event_type', 'user', 'task', 'metadata', 'timestamp']
    
    def has_add_permission(self, request):
        # Events are created automatically, not manually
        return False
    
    def has_change_permission(self, request, obj=None):
        # Events are immutable
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup
        return True
