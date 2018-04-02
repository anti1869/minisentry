from django.core.paginator import Paginator
from django.http import HttpResponseNotFound

from minisentry.models import Group, Project
from minisentry.views.projects import BaseView


class GroupsListView(BaseView):
    template_name = "groups_list.html"

    PER_PAGE = 50

    def get_context_data(self, **kwargs):
        try:
            project = Project.objects.get(pk=self.kwargs["project_id"])
        except Project.DoesNotExist:
            return HttpResponseNotFound()

        data = super().get_context_data(**kwargs)
        data.update({
            "selected_project": project,
            "groups": self.get_groups_list(project),
            "page": self.requested_page,
        })
        return data

    @property
    def requested_page(self) -> int:
        return int(self.request.GET.get("page", 1))

    def get_groups_list(self, project: Project):
        qs = Group.objects.filter(project=project).order_by("-last_seen")
        paginator = Paginator(qs, self.PER_PAGE)
        groups_list = paginator.get_page(self.requested_page)
        return groups_list


class GroupView(BaseView):
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        try:
            project = Project.objects.get(pk=self.kwargs["project_id"])
            group = Group.objects.get(long_id=kwargs["group_id"], project=project)
        except (Project.DoesNotExist, Group.DoesNotExist):
            return HttpResponseNotFound()

        event = group.get_last_event()

        data = super().get_context_data(**kwargs)
        data.update({
            "selected_project": project,
            "group": group,
            "event": event,
            "data": event.decoded_data,
        })
        return data

