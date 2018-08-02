import json
import unittest.mock

import django
import pytest

from js_urls.serializer import get_urls_as_json


class TestGetUrlsAsJsonHelper:
    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy', ])
    def test_can_serialize_specific_urls_that_do_not_have_arguments(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy'] == '/dummy/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy_with_args', ])
    def test_can_serialize_specific_urls_that_have_unnamed_arguments(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy_with_args'] == '/dummy/<>/foo/<>/bar/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy_with_kwargs', ])
    def test_can_serialize_specific_urls_that_have_named_arguments(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy_with_kwargs'] == '/dummy/<pk1>/foo/<pk2>/bar/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy_with_optional_character', ])
    def test_can_serialize_specific_urls_that_have_optional_characters(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy_with_optional_character'] == '/dummy/<>/foo/bar/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy_with_optional_group', ])
    def test_can_serialize_specific_urls_that_have_an_optional_group(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy_with_optional_group'] == '/dummy/<>/foo/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['dummy_with_optional_kwarg', ])
    def test_can_serialize_specific_urls_that_have_an_optional_kwarg(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['dummy_with_optional_kwarg'] == '/dummy/<>/'

    @unittest.mock.patch('js_urls.conf.settings.URLS', ['included_test_with_args', ])
    def test_can_serialize_specific_urls_that_have_been_included(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['included_test_with_args'] == '/included/<pk1>/test/<>/foo/<>/bar/'

    @pytest.mark.skipif(django.VERSION < (2, 0), reason='requires Django >= 2.0')
    @unittest.mock.patch('js_urls.conf.settings.URLS', ['articles_with_re_path', ])
    def test_can_serialize_specific_urls_that_have_a_regex_path(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['articles_with_re_path'] == '/articles/<year>/'

    @pytest.mark.skipif(django.VERSION < (2, 0), reason='requires Django >= 2.0')
    @unittest.mock.patch('js_urls.conf.settings.URLS', ['articles_with_path', ])
    def test_can_serialize_specific_urls_that_have_a_path_expression(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['articles_with_path'] == '/articles/<year>/'

    @pytest.mark.skipif(django.VERSION < (2, 0), reason='requires Django >= 2.0')
    @unittest.mock.patch('js_urls.conf.settings.URLS', ['articles_with_paths', ])
    def test_can_serialize_specific_urls_that_have_multiple_path_expressions(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['articles_with_paths'] == '/articles/<year>/<month>/'

    @pytest.mark.skipif(django.VERSION < (2, 0), reason='requires Django >= 2.0')
    @unittest.mock.patch('js_urls.conf.settings.URLS', ['articles_with_path_without_converter', ])
    def test_can_serialize_specific_urls_that_have_a_path_without_converter(self):
        output_dict = json.loads(get_urls_as_json())
        assert output_dict['articles_with_path_without_converter'] == '/articles/<slug>/'
