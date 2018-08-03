from django.urls import reverse
from django.utils.encoding import force_text


class TestJsUrlsView:
    def test_can_return_serialized_urls(self, client):
        response = client.get(reverse('js_urls'))
        assert force_text(response.content).startswith('window.reverse')
