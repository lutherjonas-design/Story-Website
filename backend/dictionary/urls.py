from django.urls import path
from .views import WordsToAddView, CandidatesToDictionary

urlpatterns = [ # api/dict/
    path("candidates/", WordsToAddView.as_view(), name="words-to-add-view"),
    path("transfer/",CandidatesToDictionary.as_view(), name = "dict-transfer")
]