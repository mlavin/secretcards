import binascii

from django import forms

from pgpdump.data import AsciiData
from pgpdump.utils import PgpdumpException

from . import models


class NewMessageForm(forms.ModelForm):
    """Form for creating a new message."""

    class Meta:
        model = models.Message
        fields = ('message', 'image', )
        widgets = {
            'image': forms.HiddenInput,
        }

    def clean_message(self):
        """Validate message format."""
        message = self.cleaned_data.get('message')
        if message is not None:
            try:
                len([p for p in AsciiData(message.encode('ascii')).packets()])
            except (PgpdumpException, binascii.Error):
                raise forms.ValidationError('Message is not encrypted.')
        return message
