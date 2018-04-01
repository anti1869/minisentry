import base64
import hashlib
import logging
import json
import uuid
import zlib
from gzip import GzipFile
from io import BytesIO
from typing import Tuple

from django.core.serializers.json import DjangoJSONEncoder


logger = logging.getLogger(__name__)


def gen_secret() -> str:
    return str(uuid.uuid4().hex)


def decode_data(encoded_data):
    try:
        return encoded_data.decode('utf-8')
    except UnicodeDecodeError as e:
        # This error should be caught as it suggests that there's a
        # bug somewhere in the client's code.
        logger.error(str(e), exc_info=True)


def decompress_deflate(encoded_data):
    try:
        return zlib.decompress(encoded_data).decode('utf-8')
    except Exception as e:
        # This error should be caught as it suggests that there's a
        # bug somewhere in the client's code.
        logger.error(str(e), exc_info=True)


def compress_deflate(string: str):
    return zlib.compress(string.encode('utf-8'))


def decompress_gzip(encoded_data):
    try:
        fp = BytesIO(encoded_data)
        try:
            f = GzipFile(fileobj=fp)
            return f.read().decode('utf-8')
        finally:
            f.close()
    except Exception as e:
        # This error should be caught as it suggests that there's a
        # bug somewhere in the client's code.
        logger.debug(str(e), exc_info=True)


def decompress(value):
    return zlib.decompress(base64.b64decode(value))


def decode_and_decompress_data(encoded_data):
    try:
        try:
            return decompress(encoded_data).decode('utf-8')
        except zlib.error:
            return base64.b64decode(encoded_data).decode('utf-8')
    except Exception as e:
        # This error should be caught as it suggests that there's a
        # bug somewhere in the client's code.
        logger.error(str(e), exc_info=True)


def safely_load_json_string(json_string):
    try:
        if isinstance(json_string, bytes):
            json_string = json_string.decode('utf-8')
        obj = json.loads(json_string)
        assert isinstance(obj, dict)
    except Exception as e:
        # This error should be caught as it suggests that there's a
        # bug somewhere in the client's code.
        logger.error(str(e), exc_info=True)
    else:
        return obj


def convert_to_json(obj):
    return json.dumps(obj, cls=DjangoJSONEncoder)


def hash_string(string) -> str:
    # TODO: Make it faster
    return hashlib.md5(string.encode()).hexdigest()


def choices_from_enum(source: type) -> Tuple[Tuple[int, str], ...]:
    """
    Makes tuple to use in Django's Fields ``choices`` attribute.
    Enum members names will be titles for the choices.

    :param source: Enum to process.
    :return: Tuple to put into ``choices``
    """
    result = tuple((s.value, s.name.title()) for s in source)
    return result
