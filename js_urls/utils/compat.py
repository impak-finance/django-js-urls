"""
    JS URLs compatibility utilities
    ===============================

    This modules defines utilities allowing to support multiple versions of Python and Django.

"""

import django


if django.VERSION < (2, 0):  # pragma: no cover
    from django.urls.resolvers import RegexURLPattern, RegexURLResolver
    RegexPattern = type('RegexPattern')
    RoutePattern = type('RoutePattern')
    URLResolver = RegexURLResolver
    URLPattern = RegexURLPattern
else:
    from django.urls.resolvers import (  # noqa: F401
        RegexPattern, RoutePattern, URLPattern, URLResolver,
    )
