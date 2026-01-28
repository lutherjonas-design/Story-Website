from django.test import SimpleTestCase

from .services.chapter_add import create_words_statistsics, get_words
class ServicesChapterAddTests(SimpleTestCase):
    maxDiff = None

    def test_get_words_basic(self):
        content = "Hello, world! This is a test."
        expected = ["hello", "world", "this", "is", "a", "test"]
        result = get_words(content)
        self.assertEqual(result, expected)

    def test_get_words_with_special_characters(self):
        content = "Hello-world… Testing: one, two; three?"
        expected = ["hello-world", "testing", "one", "two", "three"]
        result = get_words(content)
        self.assertEqual(result, expected)

    def test_create_words_statistics(self):
        paragraphs = [
            "Hello world",
            "Hello again, world!",
            "Testing one two three."
        ]
        expected_all_words = {
            "hello": 2,
            "world": 2,
            "again": 1,
            "testing": 1,
            "one": 1,
            "two": 1,
            "three": 1
        }
        expected_unique_words_paragraphs = [
            {"hello", "world"},
            {"hello", "again", "world"},
            {"testing", "one", "two", "three"}
        ]
        all_words, unique_words_paragraphs = create_words_statistsics(paragraph_list=paragraphs)
        self.assertEqual(all_words, expected_all_words)
        self.assertEqual(unique_words_paragraphs, expected_unique_words_paragraphs)