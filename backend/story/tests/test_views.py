import pytest #type:ignore
from django.urls import reverse
from rest_framework.test import APIClient #type:ignore
from story.models import Stories


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def url():
    return reverse("stories-list")


@pytest.mark.django_db
def test_returns_empty_list(api_client, url):
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data == []


@pytest.mark.django_db
def test_returns_stories_ordered(api_client, url):
    s1 = Stories.objects.create(title="B", description="desc B")
    s2 = Stories.objects.create(title="A", description="desc A")

    resp = api_client.get(url)
    assert [item["id"] for item in resp.data] == [s1.id, s2.id]


@pytest.mark.django_db
def test_post_not_allowed(api_client, url):
    resp = api_client.post(url, {"title": "X", "description": "Y"}, format="json")
    assert resp.status_code == 405
