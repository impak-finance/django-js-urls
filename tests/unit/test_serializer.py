import json
import unittest.mock

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
