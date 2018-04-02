from django.contrib import admin

from minisentry.models import Event, Group, Project


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('dsn',)
    list_display = ('title', 'pk')

    def dsn(self, instance):
        return instance.get_dsn()


class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'first_seen'
    list_display = ('first_seen', 'last_seen', 'type_title', 'times_seen', 'long_id')


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('timestamp', 'type_title', 'event_id')
    readonly_fields = ('decoded_data',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Group, GroupAdmin)
