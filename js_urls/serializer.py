"""
    JS URLs serializer
    ==================

    This module defiine helper functions allowing to convert the URLs that are associated with the
    names or namespaces defined in the settings to JSON. The resulting JSON will be used by a
    Javascript module to provide reverse-like functionality.

"""

import json
import re
from urllib.parse import urljoin

from django.urls import get_resolver

from .conf import settings
from .utils.compat import RegexPattern, RoutePattern, URLPattern, URLResolver
from .utils.text import replace


url_arg_re = re.compile(r'(\(.*?\))')
url_kwarg_re = re.compile(r'(\(\?P\<(.*?)\>.*?\))')
url_optional_char_re = re.compile(r'(?:\w|/)(?:\?|\*)')
url_optional_group_re = re.compile(r'\(\?\:.*\)(?:\?|\*)')
url_path_re = re.compile(r'<(.*?)>')


def get_urls_as_json(resolver=None):
    """ Returns the URLs associated with an URL resover as JSON.

    This function will traverse the tree of URLs of an URL resolver in order to return a JSON
    containing the correspondance between fully qualified URL names and the related paths. Only URLs
    that are configured to be serialized are included in the final JSON.

    """
    resolver = resolver or get_resolver()
    return json.dumps(dict(_parse_resolver(resolver)))


def _parse_resolver(resolver, current_namespace=None, url_prefix=None, include_all=False):
    ns = (
        '{}:{}'.format(current_namespace, resolver.namespace)
        if current_namespace else resolver.namespace
    )
    include_all = include_all or (ns in settings.URLS)

    urls = []
    for url_pattern in resolver.url_patterns:
        if isinstance(url_pattern, URLResolver):
            new_url_prefix = _prepare_url_part(url_pattern)
            new_url_prefix = (
                '/' + new_url_prefix if url_prefix is None else
                urljoin(url_prefix or '/', new_url_prefix)
            )
            urls = urls + _parse_resolver(
                url_pattern,
                current_namespace=ns,
                url_prefix=new_url_prefix,
                include_all=include_all,
            )
        elif isinstance(url_pattern, URLPattern) and url_pattern.name:
            url_name = '{}:{}'.format(ns, url_pattern.name) if ns else url_pattern.name
            if url_name in settings.URLS or include_all:
                full_url = _prepare_url_part(url_pattern)
                urls.append((url_name, urljoin(url_prefix or '/', full_url)))

    return urls


def _prepare_url_part(url_pattern):
    url = ''

    if hasattr(url_pattern, 'regex'):  # pragma: no cover, NOTE: Django < 2.0 compatibility
        url = url_pattern.regex.pattern
    elif isinstance(url_pattern.pattern, RegexPattern):
        url = url_pattern.pattern._regex
    elif isinstance(url_pattern.pattern, RoutePattern):
        url = url_pattern.pattern._route

    final_url = replace(url, [('^', ''), ('$', '')])

    # Removes optional groups from the URL pattern.
    optional_group_matches = url_optional_group_re.findall(final_url)
    final_url = (
        replace(final_url, [(el, '') for el in optional_group_matches])
        if optional_group_matches else final_url
    )

    # Remvoves optional characters from the URL pattern.
    optional_char_matches = url_optional_char_re.findall(final_url)
    final_url = (
        replace(final_url, [(el, '') for el in optional_char_matches])
        if optional_char_matches else final_url
    )

    # Identifies named URL arguments inside the URL pattern.
    kwarg_matches = url_kwarg_re.findall(final_url)
    final_url = (
        replace(final_url, [(el[0], '<{}>'.format(el[1])) for el in kwarg_matches])
        if kwarg_matches else final_url
    )

    # Identifies unnamed URL arguments inside the URL pattern.
    args_matches = url_arg_re.findall(final_url)
    final_url = (
        replace(final_url, [(el, '<>') for el in args_matches]) if args_matches else final_url
    )

    # Identifies path expression and associated converters inside the URL pattern.
    path_matches = url_path_re.findall(final_url)
    final_url = (
        replace(final_url, [(el, el.split(':')[-1]) for el in path_matches])
        if (path_matches and not (kwarg_matches or args_matches)) else final_url
    )

    return final_url
