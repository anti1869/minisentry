"""
Uwsgi mule is used for simple offloading long running tasks.
"""
import django
from django.apps import apps
from django.conf import settings

if not apps.ready and not settings.configured:
    django.setup()

import logging

try:
    import uwsgi
    UWSGI = True
except ImportError:
    UWSGI = False

from minisentry.email import send_group_created_email
from minisentry.helpers import convert_to_json, safely_load_json_string


logger = logging.getLogger(__name__)


def run_mule():
    """Enter mule loop. Receive tasks and executes them"""
    if not UWSGI:
        logger.error("You must be within uwsgi to run mule")
        return

    while True:
        logger.info("Mule running, Waiting for messages..")
        data = uwsgi.mule_get_msg()
        execute_task(data)


def dummy_task(**kwargs):
    """Use this one for testing mule"""
    print("Hi! I'm dummy! My kwargs are: %s", kwargs)
    return True


# TODO: Use lazy loading
TASKS = {
    "send_group_created_email": send_group_created_email,
    "test_dummy": dummy_task,
}


def send_task(name, **kwargs):
    """Serialize task data and send to mule."""
    if not UWSGI:
        logger.warning("Not running within uwsgi. Task `%s` aborted", name)
    kwargs["__task_name"] = name
    data = convert_to_json(kwargs)
    uwsgi.mule_msg(data)


def execute_task(data):
    """
    Deserialize data for task and execute it.
    This one is happening within mule.
    """
    task_data = safely_load_json_string(data)
    task_name = task_data.pop("__task_name")
    f = TASKS.get(task_name)
    if not f:
        logger.error("Can not find task with name=`%s`", task_name)
    logger.info("Executing task name=`%s`", task_name)
    result = f(**task_data)
    logger.info("Task finished with result=`%s`", result)


delayed_tasks = []


def delay_task(name, **kwargs):
    """Execute task later (use from transaction blocks)"""
    delayed_tasks.append((name, kwargs))


def send_delayed_tasks():
    """Send all delayed tasks to mules. Use this in on_commit hook"""
    for name, kwargs in delayed_tasks:
        send_task(name, **kwargs)
    delayed_tasks.clear()


if __name__ == "__main__":
    run_mule()
