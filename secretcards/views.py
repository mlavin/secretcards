import itertools

from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404, FileResponse
from django.views.generic import CreateView, DetailView, TemplateView

from . import forms, models


class HomepageView(TemplateView):
    template_name = 'home.html'


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        images = [
            (user, staticfiles_storage.url('img/kittens/{}'.format(name)))
            for name, user in models.IMAGES
        ]
        # Split into rows of 4
        args = [iter(images)] * 4
        context['images'] = itertools.zip_longest(fillvalue=None, *args)
        return context


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


class MessageDetailView(DetailView):
    template_name = 'secretcards/message-detail.html'
    model = models.Message
    context_object_name = 'message'
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def get_object(self, queryset=None):
        # Convert the URL slug into the expected UID
        self.kwargs['uid'] = int(self.kwargs['slug'], 16)
        return super().get_object(queryset=queryset)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['full_image_url'] = self.request.build_absolute_uri(
            context['message'].get_image_url())
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.content_type == 'image/png':
            message = context['message']
            image = message.get_image()
            if image is not None:
                response = FileResponse(image, content_type=self.content_type)
                if 'download' in self.request.GET:
                    response['Content-Disposition'] = 'attachment; filename={}.png'.format(
                        message.slug)
                return response
            else:
                raise Http404('Invalid/unknown image name {}.'.format(message.image))
        else:
            return super().render_to_response(context, **response_kwargs)
