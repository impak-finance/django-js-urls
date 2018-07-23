"""
    JS URLs settings
    ================

    This file defines settings that can be overriden in the Django project's settings module.

"""

from django.conf import settings


# The "JS_URLS" setting allows to define which URLs should be serialized and made available in the
# Javascript helper. It should be noted that this setting should contain only URL names or
# namespaces. URL paths associated with configured URL names will be serialized. If namespaces are
# used in the context of this setting, all the underlying URL paths will be serialized.
URLS = getattr(settings, 'JS_URLS', [])
