from django.db import models


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
