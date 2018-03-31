import logging
from django.http import HttpResponse


logger = logging.getLogger(__name__)


def store(request, project_id):
    logging.info("Got incoming request")
    import zlib
    data = request.body

    data = zlib.decompress(data).decode('utf-8')

    print(data)
    return HttpResponse({})

