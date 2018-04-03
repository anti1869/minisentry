"""
Regular tasks
"""

import logging
from datetime import timedelta

try:
    from uwsgidecorators import cron
    import uwsgi
    UWSGI = True
except ImportError:
    UWSGI = False

from django.conf import settings

from minisentry.models import Group


logger = logging.getLogger(__name__)


if UWSGI:
    from django.contrib.sessions.models import Session
    from django.utils import timezone


    @cron(18, -1, -1, -1, -1)
    def cleanup(num):
        now = timezone.now()
        logger.info("It's time for cleaning up")
        cnt, _ = Session.objects.filter(expire_date__lt=now).delete()
        logger.info("Deleted %s db rows", cnt)
        too_old = timezone.now() - timedelta(days=settings.KEEP_DATA_FOR_DAYS)
        cnt, _ = Group.objects.filter(last_seen__lte=too_old).delete()
        logger.info("Deleted %s db rows", cnt)
