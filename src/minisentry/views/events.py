from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.http import HttpResponseNotFound

from minisentry.models import Event, Project
from minisentry.views.projects import BaseView


class EventsListView(BaseView):
    template_name = "events_list.html"

    PER_PAGE = 50

    def get_context_data(self, **kwargs):
        try:
            project = Project.objects.get(pk=self.kwargs["project_id"])
        except Project.DoesNotExist:
            return HttpResponseNotFound()

        data = super().get_context_data(**kwargs)
        data.update({
            "selected_project": project,
            "events": self.get_events_list(project),
            "page": self.requested_page,
        })
        return data

    @property
    def requested_page(self) -> int:
        return int(self.kwargs.get("page", 1))

    def get_events_list1(self, project: Project):
        sql = """
            SELECT 
              "id", "group_id", "event_id", "message", "level", "timestamp",
              COUNT("group_id") AS "group_count"        
            FROM "minisentry_event"
            WHERE "project_id" = %s
            GROUP BY "group_id"
            ORDER BY "timestamp" DESC
            LIMIT %s OFFSET %s 
        """
        offset = (self.requested_page - 1) * self.PER_PAGE
        qs = (
            Event.objects
            .raw(sql, (project.pk, self.PER_PAGE, offset))
            # TODO: Why next doesnt work on SQLite? Every fields goes to GROUP BY
            # .annotate(group_count=Count("group_id"))
            # .values("group_id", "event_id", "message", "level", "timestamp")
            # .order_by("group_id")
            # .order_by("-timestamp")
        )
        # TODO: Paginator also doesn't work with this raw QS
        # paginator = Paginator(qs, self.PER_PAGE)
        # events_list = paginator.get_page(1)  # TODO: Pagination
        return qs

    def get_events_list(self, project: Project):
        qs = (
            Event.objects
            .distinct()
            .values("group_id", "event_id")
            .annotate(group_count=Count("group_id"))
            .order_by()
        )
        raise Exception(qs)
        return qs





class EventView(BaseView):
    template_name = "event.html"
