from django.http import HttpResponse

from minisentry.helpers import decompress_deflate

def mainpage(request):
    """Mainpage will redirect to browsing"""

    from minisentry.models import Event

    entry = Event.objects.last()
    from pprint import pprint
    pprint(entry.decoded_data)
    return HttpResponse()



