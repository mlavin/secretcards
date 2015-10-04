import os
import tempfile
import zipfile

from django.test import TestCase

from PIL import Image

from . import factories


class MessageTestCase(TestCase):
    """Model methods for the message model."""

    def test_slug(self):
        """Each message should have a unique slug visible to users."""
        message = factories.create_message()
        self.assertEqual(int(message.slug, 16), message.uid)
        self.assertEqual(len(message.slug), 16)

    def test_detail_url(self):
        """Messages have URLS which link to them based on their slug."""
        message = factories.create_message()
        self.assertIn(message.slug, message.get_absolute_url())

    def test_image_url(self):
        """Messages have URLS which link to the dynamic image based on their slug."""
        message = factories.create_message()
        self.assertIn(message.slug, message.get_image_url())

    def test_get_image(self):
        """Message builds a dynamic image from the original image and message."""
        message = factories.create_message()
        image = message.get_image()
        result = Image.open(image)
        result.verify()
        self.assertEqual(Image.MIME.get(result.format), 'image/png')

    def test_get_image_message(self):
        """Message image contains an embedded zip with the message body."""
        message = factories.create_message()
        image = message.get_image()
        _, filename = tempfile.mkstemp()
        try:
            with open(filename, 'wb') as f:
                f.write(image.read())
            result = zipfile.ZipFile(filename)
            expected = '{}.asc'.format(message.slug)
            self.assertEqual(result.namelist(), [expected, ])
            with result.open(expected) as msgfile:
                self.assertEqual(msgfile.read().decode('ascii'), message.message)
        finally:
            os.remove(filename)

    def test_get_invalid_image(self):
        """Handle the case of corrupt model data/missing images."""
        message = factories.create_message(image='invalid')
        self.assertIsNone(message.get_image())
