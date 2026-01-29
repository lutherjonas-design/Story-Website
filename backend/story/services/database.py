from ..models import Chapters, Paragraphs,Dictionary, UniqueWordsInParagraphs, WordsToAdd
# Creates a chapter with the next number and its paragraphs atomically.
# Assumes story and paragraph_list are already validated.
def create_chapter_atomic(*, story, title, paragraph_list, words_to_add, chapter_word_set) -> Chapters:
    from django.db import transaction
    from django.db.models import Max,F, Case, When, Value, IntegerField
    from .chapter_add import title_words_statistics

    with transaction.atomic():
        last_num = (
            Chapters.objects.select_for_update()
            .filter(story=story)
            .aggregate(m=Max("chapter_order"))["m"]
        )
        next_number = (last_num or 0) + 1

        chapter = Chapters.objects.create(
            title=title,
            story=story,
            chapter_order=next_number,
            dictionary_completed=False,
        )

        Paragraphs.objects.bulk_create(
            Paragraphs(
                chapter=chapter,
                number=i+1,
                content=block,
            )
            for i, block in enumerate(paragraph_list)
        )

        para_objs = list(
            Paragraphs.objects.filter(chapter=chapter).order_by('number')
        )
        # Sanity alignment: chapter_word_set must match paragraph_list length
        if len(para_objs) != len(chapter_word_set):
            raise ValueError("chapter_word_set length mismatch paragraph_list")
        # Create UniqueWordsInParagraphs
        uip_bulk = []
        for p_obj, uw_set in zip(para_objs, chapter_word_set):
            for w in uw_set:
                # Lowercased already by tokenizer; UniqueConstraint(Lower('word'), paragraph) enforces uniqueness
                uip_bulk.append(UniqueWordsInParagraphs(
                    paragraph=p_obj, word=w))

        UniqueWordsInParagraphs.objects.bulk_create(
            uip_bulk, ignore_conflicts=True)
        
        for words in title_words_statistics(title=title):
            words_to_add[words] = words_to_add.get(words, 0) + 1

        if words_to_add:
            existing_words = set(
                Dictionary.objects
                .filter(word__in=words_to_add.keys())
                .values_list("word", flat=True)
            )
            words_that_need_syllables = {
                word: freq
                for word, freq in words_to_add.items()
                if word not in existing_words
            }
            existing = set(
                WordsToAdd.objects.filter(word__in=words_that_need_syllables.keys()).values_list('word', flat=True)
            )
            to_update = {
                word: freq
                for word, freq in words_that_need_syllables.items()
                if word in existing
            }
            if to_update:           
                whens = [When(word=w, then=Value(freq)) for w, freq in to_update.items()]
                WordsToAdd.objects.filter(word__in=to_update.keys()).update(
                    frequency=F('frequency') + Case(*whens, default=Value(0), output_field=IntegerField())
                )

            to_create = {
                word: freq
                for word, freq in words_that_need_syllables.items()
                if word not in existing
            }
            if to_create:
                WordsToAdd.objects.bulk_create(
                    (WordsToAdd(word=word, frequency=freq) for word, freq in to_create.items()),
                    ignore_conflicts=True
                )

    return chapter