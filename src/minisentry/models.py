import logging
from enum import Enum

from django.db import models

from minisentry.constants import LOG_LEVELS
from minisentry.helpers import (
    choices_from_enum, gen_secret, safely_load_json_string, decompress_deflate
)


class GroupStatus(Enum):
    UNRESOLVED = 0
    RESOLVED = 1
    IGNORED = 2
    PENDING_DELETION = 3
    DELETION_IN_PROGRESS = 4
    PENDING_MERGE = 5


GROUP_CHOICES = choices_from_enum(GroupStatus)


class Project(models.Model):
    """Project"""
    title = models.CharField(max_length=255)
    key = models.CharField(default=gen_secret, max_length=34)
    secret = models.CharField(default=gen_secret, max_length=34)

    def get_dsn(self) -> str:
        # TODO: Extract real schema and host
        result = "{schema}://{key}:{secret}@{host}/{project_id}".format(
            schema="http",
            key=self.key,
            secret=self.secret,
            host="localhost:8000",
            project_id=self.pk,
        )
        return result

    def __str__(self):
        return f"id={self.pk}, {self.title}"


class Group(models.Model):
    """
    Aggregated message which summarizes a set of Events.
    """
    long_id = models.CharField(max_length=32, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    level = models.IntegerField(
        choices=LOG_LEVELS.items(), default=logging.ERROR, blank=True, db_index=True
    )
    message = models.TextField()
    platform = models.CharField(max_length=64, null=True)
    status = models.PositiveIntegerField(
        default=GroupStatus.UNRESOLVED.value,
        choices=GROUP_CHOICES,
        db_index=True
    )    
    times_seen = models.PositiveIntegerField(default=1, db_index=True)
    last_seen = models.DateTimeField(auto_now_add=True, db_index=True)
    first_seen = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, db_index=True)

    class Meta:
        index_together = (("project", "last_seen"), )
        ordering = ["-last_seen"]
        
    def last_event(self) -> "Event":
        return self.event_set.latest("timestamp")


class Event(models.Model):
    """
    An individual event.
    """
    event_id = models.CharField(max_length=32)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, to_field="long_id")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    level = models.IntegerField(null=True)
    platform = models.CharField(max_length=64, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    time_spent = models.IntegerField(null=True)
    data = models.BinaryField()

    class Meta:
        unique_together = (('project', 'event_id'),)
        index_together = (('group', 'timestamp'),)
        ordering = ["-timestamp"]

    @property
    def decoded_data(self):
        if not hasattr(self, "_decoded_data"):
            setattr(
                self, "_decoded_data",
                safely_load_json_string(decompress_deflate(self.data))
            )
        return getattr(self, "_decoded_data")
