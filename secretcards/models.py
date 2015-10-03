from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
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

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        return reverse('message-image', kwargs={'slug': self.slug})

    @property
    def slug(self):
        return '{0:x}'.format(self.uid)

    @property
    def image_buffer(self):
        """File buffer for image + encrypted message."""
        image_path = finders.find('img/kittens/{}'.format(self.image))
        if image_path:
            return open(image_path, 'rb')
        else:
            return None
