from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from minisentry.views import auth, coreapi, events, projects


urlpatterns = [
    path("", auth.mainpage, name="mainpage"),
    path("admin/", admin.site.urls),
    path("sentry/", projects.ProjectsListView.as_view(), name="projects-list"),
    path("sentry/<project_id>/", projects.ProjectView.as_view(), name="project"),
    path("sentry/<project_id>/events/", events.EventsListView.as_view(), name="events-list"),
    path("sentry/<project_id>/events/<event_id>/", events.EventView.as_view(), name="events"),
    path("api/<project_id>/store/", coreapi.store, name="store"),
]

if settings.USE_SILK:
    urlpatterns.append(
        url(r'^silk/', include('silk.urls', namespace='silk'))
    )
