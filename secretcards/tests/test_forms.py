from django.test import SimpleTestCase

from .. import forms
from . import factories


class NewMessageFormTestCase(SimpleTestCase):
    """Form validation for creating messages."""

    def test_valid_data(self):
        """Basic valid data."""
        data = factories.get_message_data()
        form = forms.NewMessageForm(data)
        self.assertTrue(form.is_valid())

    def test_require_data(self):
        """Image and message are required."""
        for name in ('image', 'message'):
            data = factories.get_message_data()
            del data[name]
            form = forms.NewMessageForm(data)
            self.assertFalse(form.is_valid())

    def test_invalid_image(self):
        """Handle invalid image name."""
        data = factories.get_message_data()
        data['image'] = 'invalid'
        form = forms.NewMessageForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_message(self):
        """Reject messages which aren't encrypted."""
        data = factories.get_message_data()
        data['message'] = 'invalid'
        form = forms.NewMessageForm(data)
        self.assertFalse(form.is_valid())
