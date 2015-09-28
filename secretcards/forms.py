from django import forms

from . import models


class NewMessageForm(forms.ModelForm):
    """Form for creating a new message."""

    class Meta:
        model = models.Message
        fields = ('message', 'image', )

    def clean_message(self):
        """Validate message format."""
        message = self.cleaned_data.get('message')
        if message is not None:
            pass
        return message
