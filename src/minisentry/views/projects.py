from typing import Dict, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy


class BaseView(LoginRequiredMixin, TemplateView):
    """Base class for all browsing views"""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["projects"] = self.get_projects_menu()
        return data

    def get_projects_menu(self) -> List[Dict]:
        data = [
            # {
            #     "title": title,
            #     "url": url,
            #     "hit": self.request.path == url,
            # } for title, url in self.sidebar_menu
        ]
        return data


class ProjectsListView(BaseView):
    template_name = "projects_list.html"


class ProjectView(BaseView):
    template_name = "project_list.html"


