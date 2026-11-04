
# story/tests/test_stories_list_view.py
import pytest #type:ignore
from django.urls import reverse
from story.models import Stories

@pytest.mark.django_db
class TestStoryView:
    @pytest.fixture
    def url(self):
        return reverse("story-detail")

    def test_returns_empty_list(self, api_client, url):
        resp = api_client.get(url)
        assert resp.status_code == 200
        assert resp.data == []

    def test_returns_stories_ordered_by_id(self, api_client, url):
        s1 = Stories.objects.create(title="B", description="desc B")
        s2 = Stories.objects.create(title="A", description="desc A")
        resp = api_client.get(url)
        assert [item["id"] for item in resp.data] == [s1.id, s2.id]

    def test_item_shape(self, api_client, url):
        Stories.objects.create(title="T", description="D")
        resp = api_client.get(url)
        assert resp.status_code == 200
        assert set(resp.data[0].keys()) == {"id", "title", "description"}

    def test_post_not_allowed(self, api_client, url):
        resp = api_client.post(url, {"title": "X", "description": "Y"}, format="json")
        assert resp.status_code == 405
