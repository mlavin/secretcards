import random

from .. import models


def create_message(**kwargs):
    """Create a test message."""
    values = {
        'message': '',
        'image': random.choice([i[0] for i in models.IMAGES])
    }
    values.update(kwargs)
    return models.Message.objects.create(**values)
