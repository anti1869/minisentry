import logging

from django.contrib.auth.models import User
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings
from django.template import loader

from minisentry.models import Group, Event


logger = logging.getLogger(__name__)


def send_group_created_email(group_id: str):
    """Send email with new exception event group"""
    try:
        group = Group.objects.select_related("project").get(long_id=group_id)
    except Group.DoesNotExist:
        logger.error("Can't find group with long_id=%s", group_id)
        return

    last_event = group.get_last_event()
    emails = User.objects.filter(email__isnull=False).values_list("email", flat=True)

    subject = f"[MiniSentry] [{group.project.title}] {group.last_seen} {group.type_exc[0]}"

    # Prepare message body
    ctx = {
        "project": group.project,
        "group": group,
        "data": last_event.decoded_data,
        "url_prefix": settings.MINISENTRY_URL_PREFIX,
    }
    template = loader.get_template("emails/group_created.html")
    html_message = template.render(ctx)
    text_message = "Please, view HTML version of this message. Plain text is not supported yet."

    send_mass_mail_multi(
        subject, settings.DEFAULT_FROM_EMAIL_FULL, emails,
        text_message, html_message
    )


def send_mass_mail_multi(subject, from_email, emails,
              text_message, html_message,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    logger.info("Sending %s email(s)", len(emails))
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    if len(emails) > 20:
        logger.warning(
            "MiniSentry was not supposed to handle so much users. "
            "Performance may be sluggish."
        )
    messages = []
    for email in emails:
        message = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=from_email,
            to=(email, ),
            headers={},
        )
        message.attach_alternative(html_message, "text/html")
        messages.append(message)
    result = connection.send_messages(messages)
    connection.close()
    return result



