
# story/tests/conftest.py
import pytest #type:ignore
from rest_framework.test import APIClient #type:ignore
from story.models import Stories, Chapters

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def make_story():
    """
    Factory: create a Story.
    Usage: s = make_story(title="A", description="B")
    """
    def _make_story(title="Story", description="Desc"):
        return Stories.objects.create(title=title, description=description)
    return _make_story

@pytest.fixture
def make_chapter():
    """
    Factory: create a Chapter for a given story or a new one.
    Usage: c = make_chapter(story=s, order=1, title="Intro", dictionary_completed=True)
    If `story` is omitted, a new Story is created implicitly.
    """
    def _make_chapter(*, story=None, title="Chapter", order=1, dictionary_completed=False):
        if story is None:
            story = Stories.objects.create(title="Auto Story", description="Auto")
        return Chapters.objects.create(
            story=story,
            title=title,
            order=order,
            dictionary_completed=dictionary_completed,
        )
    return _make_chapter