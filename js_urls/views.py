"""
    JS URLs views
    =============

    This module defines views allowing to expose the Javascript helper and catalog of URLs allowing
    to provide reverse-like functionality on the client side.

"""

from django.views.generic import TemplateView

from .serializer import get_urls_as_json


class JsUrlsView(TemplateView):
    """ Renders a Javascript helper allowing to reverse Django URLs. """

    content_type = 'application/javascript'
    template_name = 'js_urls/js_urls.js'

    def get_context_data(self, **kwargs):
        """ Returns the context data to provide to the template. """
        context = super().get_context_data(**kwargs)
        context['urls'] = get_urls_as_json()
        return context
