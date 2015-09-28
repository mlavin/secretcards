import itertools

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import CreateView, TemplateView

from . import forms, models


class HomepageView(TemplateView):
    template_name = 'home.html'


class MessageAddView(CreateView):
    template_name = 'secretcards/message-add.html'
    model = models.Message
    form_class = forms.NewMessageForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        images = [
            (name, staticfiles_storage.url('img/kittens/{}'.format(name)))
            for name, _ in models.IMAGES
        ]
        # Split into rows of 4
        args = [iter(images)] * 4
        context['images'] = itertools.zip_longest(fillvalue=None, *args)
        return context
