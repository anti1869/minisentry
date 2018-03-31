from minisentry.views.projects import BaseView


class EventsListView(BaseView):
    template_name = "events_list.html"


class EventView(BaseView):
    template_name = "event_list.html"