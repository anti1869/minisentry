from django.contrib import admin

from minisentry.models import Project


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('dsn',)

    def dsn(self, instance):
        return instance.get_dsn()


admin.site.register(Project, ProjectAdmin)
