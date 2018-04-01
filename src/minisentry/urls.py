from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from minisentry.views import auth, api, events, projects


urlpatterns = [
    path("", projects.mainpage, name="mainpage"),
    path("admin/", admin.site.urls),
    path("signin/", auth.SignInView.as_view(), name="signin"),
    path("signout/", auth.SignOutView.as_view(), name="signout"),
    path("sentry/", projects.DashboardView.as_view(), name="dashboard"),
    path("sentry/<project_id>/", projects.ProjectView.as_view(), name="project"),
    path("sentry/<project_id>/events/", events.EventsListView.as_view(), name="events-list"),
    path("sentry/<project_id>/events/<event_id>/", events.EventView.as_view(), name="events"),
    path("api/<project_id>/store/", api.store, name="store"),
]

if settings.USE_SILK:
    urlpatterns.append(
        url(r'^silk/', include('silk.urls', namespace='silk'))
    )
