from ..models import Chapter, Paragraph, UniqueWordsInParagraph

# Creates a chapter with the next number and its paragraphs atomically.
# Assumes story and paragraph_list are already validated.
def create_chapter_atomic(*, story, title, paragraph_list, words_to_add, chapter_word_set) -> Chapter:
    from django.db import transaction
    from django.db.models import Max
    from .chapter_add import title_words_statistics
    from dictionary.services import add_words_dict_frequency as dict_add_word

    with transaction.atomic():
        last_num = (
            Chapter.objects.select_for_update()
            .filter(story=story)
            .aggregate(m=Max("chapter_order"))["m"]
        )
        next_number = (last_num or 0) + 1

        chapter = Chapter.objects.create(
            title=title,
            story=story,
            chapter_order=next_number,
            dictionary_completed=False,
        )

        Paragraph.objects.bulk_create(
            Paragraph(
                chapter=chapter,
                number=i+1,
                content=block,
            )
            for i, block in enumerate(paragraph_list)
        )

        para_objs = list(
            Paragraph.objects.filter(chapter=chapter).order_by('number')
        )
        # Sanity alignment: chapter_word_set must match paragraph_list length
        if len(para_objs) != len(chapter_word_set):
            raise ValueError("chapter_word_set length mismatch paragraph_list")
        # Create UniqueWordsInParagraphs
        uip_bulk = []
        for p_obj, uw_set in zip(para_objs, chapter_word_set):
            for w in uw_set:
                # Lowercased already by tokenizer; UniqueConstraint(Lower('word'), paragraph) enforces uniqueness
                uip_bulk.append(UniqueWordsInParagraph(
                    paragraph=p_obj, word=w))

        UniqueWordsInParagraph.objects.bulk_create(
            uip_bulk, ignore_conflicts=True)
        
        for words in title_words_statistics(title=title):
            words_to_add[words] = words_to_add.get(words, 0) + 1

        dict_add_word(words_to_add=words_to_add)
    return chapter