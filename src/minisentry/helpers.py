import uuid


def gen_secret() -> str:
    return str(uuid.uuid4().hex)
