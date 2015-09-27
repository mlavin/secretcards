from django.db import models
from django.utils.timezone import now

from simpleflake import simpleflake


IMAGES = (
    # Filename, Username
    ('blue-eyes.png', 'sue_salisbury-maui-hawaii'),
    ('nose.png', 'comedynose'),
    ('black.png', '11638547@N00'),
    ('pair.png', 'crsan'),
    ('flying.png', 'sadie_16'),
    ('looking-up.png', 'albaraa'),
    ('gray.png', 'mtrichardson'),
    ('three.png', 'londonlooks'),
)


class Message(models.Model):
    """Encrypted message for a particular user."""

    uid = models.BigIntegerField(default=simpleflake, unique=True, db_index=True)
    message = models.TextField()
    image = models.CharField(choices=IMAGES, max_length=200)
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return 'Message {} sent on {}'.format(self.uid, self.created_date.isoformat())
