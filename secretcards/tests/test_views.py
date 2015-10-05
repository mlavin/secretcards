from django.core.urlresolvers import reverse
from django.test import override_settings, TestCase

from .. import models
from . import factories


class ViewTestMixin(object):
    """Helpers for testing views."""

    def assert_status(self, response, expected):
        self.assertEqual(response.status_code, expected)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class HomepageTestCase(ViewTestMixin, TestCase):
    """Homepage view."""

    def test_render_homepage(self):
        """Fetch the homepage."""
        with self.assertTemplateUsed('home.html'):
            response = self.client.get(reverse('home'))
            self.assert_status(response, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AddMessageTestCase(ViewTestMixin, TestCase):
    """View for creating new messages."""

    def test_render_page(self):
        """Fetch the form."""
        with self.assertTemplateUsed('secretcards/message-add.html'):
            response = self.client.get(reverse('add-message'))
            self.assert_status(response, 200)

    def test_create_message(self):
        """Create a new message object."""
        data = factories.get_message_data()
        response = self.client.post(reverse('add-message'), data=data)
        message = models.Message.objects.latest('created_date')
        self.assertRedirects(response, message.get_absolute_url())


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ViewMessageTestCase(ViewTestMixin, TestCase):
    """Message detail view."""

    def setUp(self):
        self.message = factories.create_message()

    def test_render_message(self):
        """View the details of a message."""
        with self.assertTemplateUsed('secretcards/message-detail.html'):
            response = self.client.get(self.message.get_absolute_url())
            self.assert_status(response, 200)

    def test_invalid_uid(self):
        """Handle messages which don't exist."""
        url = self.message.get_absolute_url()
        self.message.delete()
        response = self.client.get(url)
        self.assert_status(response, 404)


class MessageImageTestCase(ViewTestMixin, TestCase):
    """Dynamically generated images with messages."""

    def setUp(self):
        self.message = factories.create_message()

    def test_get_image(self):
        """Fetch the image."""
        response = self.client.get(self.message.get_image_url())
        self.assert_status(response, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_unknown_image(self):
        """Handle messages with bad images."""
        self.message.image = 'invalid'
        self.message.save()
        response = self.client.get(self.message.get_image_url())
        self.assert_status(response, 404)

    def test_download_image(self):
        """Download the image."""
        response = self.client.get(self.message.get_download_url())
        self.assert_status(response, 200)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename={}.png'.format(self.message.slug))
