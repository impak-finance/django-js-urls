"""
    JS URLs app config
    ==================

    This module contains the application configuration class - available in the Django app registry.
    For more information on this file, see https://docs.djangoproject.com/en/dev/ref/applications/

"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JSUrlsAppConfig(AppConfig):
    label = 'js_urls'
    name = 'js_urls'
    verbose_name = _('Javascript URLs')
