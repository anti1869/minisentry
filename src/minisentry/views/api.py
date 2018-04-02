import json
import logging
import uuid
from copy import deepcopy
from typing import Dict, Optional

from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import F

from minisentry import helpers
from minisentry.models import Event, Group, Project, GroupStatus


logger = logging.getLogger(__name__)


@require_POST
def store(request, project_id):
    """
    Process incoming event.
    """
    auth_header = request.META.get("HTTP_X_SENTRY_AUTH")
    try:
        project_id = int(project_id)
    except ValueError:
        return HttpResponseForbidden()

    project_id = _get_project_id_from_auth(auth_header, project_id)
    if project_id is None:
        return HttpResponseForbidden()

    content_encoding = request.META.get("HTTP_CONTENT_ENCODING")
    data = _decode_data(request.body, content_encoding)
    group = _save_group(data, project_id)
    _save_event(data, project_id, group)
    logger.info("Event saved")

    result = {"id": data.get("event_id")}
    return JsonResponse(result)


def _decode_data(data, content_encoding: str):
    """
    Decodes input data from whatever format it comes from to dict.
    """
    if isinstance(data, bytes):
        if content_encoding == 'gzip':
            data = helpers.decompress_gzip(data)
        elif content_encoding == 'deflate':
            data = helpers.decompress_deflate(data)
        elif data[0] != b'{':
            data = helpers.decode_and_decompress_data(data)
        else:
            data = helpers.decode_data(data)

    if isinstance(data, str):
        data = helpers.safely_load_json_string(data)

    return data


def _get_project_id_from_auth(auth_header: str, requested_id: int) -> Optional[int]:
    """
    Returns same project id as requested, if all checks are ok, otherwise - None
    """
    try:
        auth_data = {
            key.strip(): value
            for key, value in map(lambda x: x.split("="), auth_header.split(","))
        }
        project_id = Project.objects.filter(
            key=auth_data["sentry_key"],
            secret=auth_data["sentry_secret"],
            pk=requested_id,
        ).values_list("pk", flat=True).first()
    except (KeyError, AttributeError):
        logger.error("Wrong auth header")
        return

    return project_id


def _save_group(data: Dict, project_id: int) -> str:
    """Save event group to database and return long_id of the group"""
    long_id = _get_group_id(data, project_id)
    updated = (
        Group.objects
        .filter(long_id=long_id, project=project_id)
        .update(
            last_seen=data["timestamp"],
            times_seen=F("times_seen") + 1,
            status=GroupStatus.UNRESOLVED.value,
        )
    )
    if not updated:
        Group.objects.create(
            long_id=long_id,
            project_id=project_id,
            level=data["level"],
            message=data["message"],
            platform=data["platform"],
        )
    return long_id


def _save_event(data: Dict, project_id: int, group_id: str):
    """Save event to database"""
    kwargs = {
        name: data[name]
        for name in ("event_id", "message", "level", "platform", "timestamp", "time_spent")
    }
    kwargs["project_id"] = project_id
    kwargs["data"] = helpers.compress_deflate(helpers.convert_to_json(data))
    kwargs["group_id"] = group_id
    Event.objects.create(**kwargs)


def _get_group_id(data: Dict, project_id) -> str:
    """Generate group_id to group same events"""
    # TODO: Slow as hell. Make it faster
    # TODO: Not tested at all, have no idea if it works.
    if "exception" not in data:
        logger.info("No exception data, using UUID for group_id")
        return str(uuid.uuid4())

    try:
        exc = deepcopy(data["exception"])
        for value in exc["values"]:
            for frame in value["stacktrace"]["frames"]:
                frame.pop("vars")
        exception = json.dumps({"e": exc, "pid": project_id}, sort_keys=True)
    except (KeyError, ValueError):
        logger.error("Can't serialize exception, using UUID for group_id", exc_info=True)
        return str(uuid.uuid4())
    return helpers.hash_string(exception)
