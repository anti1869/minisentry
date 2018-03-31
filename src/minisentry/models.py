from django.db import models

from minisentry.helpers import gen_secret


class Event(models.Model):
    """
    An individual event.
    """
    group_id = models.BigIntegerField(blank=True, null=True, db_index=True)
    event_id = models.CharField(max_length=32)
    project_id = models.IntegerField()
    message = models.TextField()
    platform = models.CharField(max_length=64, null=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    time_spent = models.IntegerField(null=True)
    data = models.BinaryField()


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
