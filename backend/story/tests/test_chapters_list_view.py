# story/tests/test_chapters_list_view.py
import pytest #type:ignore
from django.urls import reverse

@pytest.mark.django_db
class TestChaptersListView:
    @pytest.fixture
    def url(self, make_story):
        story = make_story(title="Base", description="D")
        return reverse("chapters-list", kwargs={"story_id": story.id})

    def test_returns_empty_list_when_no_chapters(self, api_client, url):
        resp = api_client.get(url)
        assert resp.status_code == 200
        assert resp.data == []

    def test_lists_only_chapters_for_requested_story(self, api_client, make_story, make_chapter):
        story = make_story(title="Main")
        other = make_story(title="Other")

        c1 = make_chapter(story=story, order=2, title="Two")
        c2 = make_chapter(story=story, order=1, title="One")
        _  = make_chapter(story=other, order=1, title="Other One")  # must be excluded

        url = reverse("chapters-list", kwargs={"story_id": story.id})
        resp = api_client.get(url)

        assert resp.status_code == 200
        assert [item["title"] for item in resp.data] == ["One", "Two"]
        assert [item["id"] for item in resp.data] == [c2.id, c1.id]

    def test_item_shape(self, api_client, make_story, make_chapter):
        story = make_story()
        make_chapter(story=story, order=1, title="Intro", dictionary_completed=True)

        url = reverse("chapters-list", kwargs={"story_id": story.id})
        resp = api_client.get(url)

        assert resp.status_code == 200
        assert set(resp.data[0].keys()) == {"id", "title", "order", "dictionary_completed"}

    def test_post_not_allowed(self, api_client, make_story):
        story = make_story()
        url = reverse("chapters-list", kwargs={"story_id": story.id})
        resp = api_client.post(url, {"title": "X", "order": 1}, format="json")
        assert resp.status_code == 405
        
    def test_404_when_story_does_not_exist(self, api_client):
        url = reverse("chapters-list", kwargs={"story_id": 999999})
        resp = api_client.get(url)
        assert resp.status_code == 404

    def test_200_empty_list_when_no_chapters(self, api_client, make_story):
        story = make_story()
        url = reverse("chapters-list", kwargs={"story_id": story.id})
        resp = api_client.get(url)
        assert resp.status_code == 200
        assert resp.data == []

    def test_orders_by_order_field(self, api_client, make_story, make_chapter):
        story = make_story()
        c2 = make_chapter(story=story, order=2, title="Two")
        c1 = make_chapter(story=story, order=1, title="One")
        url = reverse("chapters-list", kwargs={"story_id": story.id})
        resp = api_client.get(url)
        assert [item["id"] for item in resp.data] == [c1.id, c2.id]
