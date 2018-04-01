from typing import Dict, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy

from minisentry.models import Project


class BaseView(LoginRequiredMixin, TemplateView):
    """Base class for all browsing views"""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["projects_menu"] = self.get_projects_menu()
        return data

    def get_projects_menu(self) -> List[Dict]:
        projects = (
            (pk, title, reverse("groups-list", kwargs={"project_id": pk}))
            for title, pk in Project.objects.values_list("title", "pk").order_by("title").iterator()
        )
        data = [
            {
                "id": pk,
                "title": title,
                "url": url,
                "hit": self.request.path == url,
            } for pk, title, url in projects
        ]
        return data


def mainpage(request):
    """Mainpage will redirect to browsing"""
    return HttpResponseRedirect(reverse("dashboard"))


class DashboardView(BaseView):
    template_name = "dashboard.html"


class ProjectView(BaseView):
    template_name = "project_list.html"


