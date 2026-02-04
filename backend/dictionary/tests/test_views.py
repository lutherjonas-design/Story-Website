
import json
from django.test import TestCase
from django.urls import reverse
from dictionary.models import WordsToAdd, Dictionary

class CandidatesToDictionaryTests(TestCase):
    maxDiff = None
    def test_stored_ok(self):
        w = WordsToAdd.objects.create(word="hello", frequency=1)

        url = reverse("dict-transfer")
        payload = {"id": w.id, "syllables": ["hel", "lo"]}

        res = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body, {"word": "hello", "syllable_breaks": [3]})

        self.assertFalse(WordsToAdd.objects.filter(id=w.id).exists())
        d = Dictionary.objects.get(word="hello")
        self.assertEqual(d.syllable_breaks, [3])

    def test_not_in_db_404(self):
        url = reverse("dict-transfer")
        payload = {"id": 999999, "syllables": ["hel", "lo"]}

        res = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        # NotFound raised in serializer → DRF default 404 with {"detail": "..."}
        self.assertEqual(res.status_code, 404)
        body = res.json()
        self.assertIn("detail", body)

    def test_invalid_data_400(self):
        w = WordsToAdd.objects.create(word="world", frequency=1)

        url = reverse("dict-transfer")
        # Syllables don't match "world" → 400 with {"errors": {...}}
        payload = {"id": w.id, "syllables": ["hel", "lo"]}

        res = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        body = res.json()
        self.assertIn("errors", body)
        self.assertIn("syllables", body["errors"])
