import io
import zipfile

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.urls import reverse
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


class _FileStream(object):
    """Yield multiple file objects together."""

    def __init__(self, files):
        self.pending = files
        self.complete = []

    def read(self, size=None):
        remaining = size
        current = io.BytesIO()
        while self.pending and (remaining is None or remaining > 0):
            chunk = self.pending[0].read(remaining or -1)
            if remaining is None or len(chunk) < remaining:
                self.complete.append(self.pending.pop(0))
            if remaining is not None:
                remaining -= len(chunk)
            current.write(chunk)
        return current.getvalue()


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

    def get_original_image_url(self):
        return staticfiles_storage.url('img/kittens/{}'.format(self.image))

    def get_download_url(self):
        return '{}?download=png'.format(self.get_image_url())

    @property
    def slug(self):
        return '{0:x}'.format(self.uid)

    def get_image(self):
        """File buffer for image + encrypted message."""
        image_path = finders.find('img/kittens/{}'.format(self.image))
        if image_path:
            zip_stream = io.BytesIO()
            zip_data = zipfile.ZipFile(zip_stream, mode='w')
            zip_data.writestr('{}.asc'.format(self.slug), self.message)
            zip_data.close()
            zip_stream.seek(0)
            return _FileStream([open(image_path, 'rb'), zip_stream])
        else:
            return None
