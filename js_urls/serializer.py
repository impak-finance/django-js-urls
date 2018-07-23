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
from django.urls.resolvers import RegexURLPattern, RegexURLResolver

from .conf import settings
from .utils.text import replace


url_kwarg_re = re.compile(r'(\(\?P\<(.*?)\>.*?\))')
url_arg_re = re.compile(r'(\(.*?\))')


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
        if isinstance(url_pattern, RegexURLResolver):
            new_url_prefix = _prepare_url_part(url_pattern.regex.pattern)
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
        elif isinstance(url_pattern, RegexURLPattern) and url_pattern.name:
            url_name = '{}:{}'.format(ns, url_pattern.name) if ns else url_pattern.name
            if url_name in settings.URLS or include_all:
                full_url = _prepare_url_part(url_pattern.regex.pattern)
                urls.append((url_name, urljoin(url_prefix or '/', full_url)))

    return urls


def _prepare_url_part(url):
    full_url = replace(url, [('^', ''), ('$', '')])

    # Identifies named URL arguments inside the URL pattern.
    kwarg_matches = url_kwarg_re.findall(full_url)
    full_url = (
        replace(full_url, [(el[0], '<{}>'.format(el[1])) for el in kwarg_matches])
        if kwarg_matches else full_url
    )

    # Identifies unnamed URL arguments inside the URL pattern.
    args_matches = url_arg_re.findall(full_url)
    full_url = replace(full_url, [(el, '<>') for el in args_matches]) if args_matches else full_url

    return full_url
