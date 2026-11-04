from typing import Tuple, Dict, Set

def create_words_statistsics(*, paragraph_list: list[str]) -> Tuple[Dict[str, int], list[Set[str]]]:
    from .reformatting_text import get_words as service_get_words
    all_words = {}
    unique_words_paragraphs = []
    for paragraph in paragraph_list:
        words = service_get_words(paragraph)
        unique_words_paragraphs.append(set(map(lambda w: w.lower(), words)))
        for word in words:
            all_words[word] = all_words.get(word, 0) + 1
    return all_words,unique_words_paragraphs

def title_words_statistics(*, title: str) -> Dict[str, int]:
    from .reformatting_text import get_words as service_get_words
    words = service_get_words(title)
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count
