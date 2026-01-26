from django.db import transaction
from django.db.models import Max

from ..models import Chapters, Paragraphs

import re

def split_paragraphs(content: str) -> list[str]:
        # 1) Normalize line endings
        text = content.replace("\r\n", "\n").replace("\r", "\n").strip()
        # exit if empty
        if not text:
            return []
        # 2) If we already have blank-line separators, use those
        if "\n\n" in text:
            blocks = [b.strip() for b in re.split(r"\n\s*\n", text)]
            return [b for b in blocks if b]
        # 3) No blank lines present -> the file may be single-newline paragraphs or hard-wrapped lines
        lines = [ln.strip() for ln in text.split("\n")]
        # Heuristic A: if the majority of lines are "long" (e.g., > 120 chars), it’s probably one paragraph with hard wraps;
        # we’ll merge lines until we detect a paragraph boundary.
        long_lines = sum(1 for ln in lines if len(ln) >= 120)
        proportion_long = long_lines / max(1, len(lines))
        # Heuristic B: treat **single newline as a paragraph break** iff the next line **looks like a new paragraph start**:
        # - starts with uppercase or a heading marker
        # - or the previous line ends with sentence-ending punctuation
        paras = []
        buf = []
        def flush():
            if buf:
                paras.append(" ".join(buf).strip())
                buf.clear()
        for i, ln in enumerate(lines):
            if not ln:
                # unexpected empty line: treat as paragraph boundary
                flush()
                continue
            buf.append(ln)
            # look-ahead
            next_ln = lines[i + 1] if i + 1 < len(lines) else ""
            ends_sentence = bool(re.search(r'[.!?]["”\')\]]?$', ln))
            next_looks_new = (
                next_ln
                and (
                    next_ln[:1].isupper()
                    or re.match(r'^(#{1,6}\s|Kapitel\b|Chapter\b|\d+[\.)]\s)', next_ln)
                )
            )
            # Decision:
            # - If we have clear sentence end and next looks like a paragraph start, break here.
            # - If lines are generally short (not “hard wrapped”), treat single newline as paragraph break.
            should_break = False
            if ends_sentence and next_looks_new:
                should_break = True
            elif proportion_long < 0.25:  # most lines are not long; likely each line = one paragraph
                should_break = True
            if should_break:
                flush()
        flush()
        return [p for p in paras if p]


# Creates a chapter with the next number and its paragraphs atomically.
# Assumes story and paragraph_list are already validated.
def create_chapter_atomic(*, story, title, paragraph_list):
    with transaction.atomic():
        last_num = (
            Chapters.objects.select_for_update()
            .filter(story=story)
            .aggregate(m=Max("number"))["m"]
        )
        next_number = (last_num or 0) + 1

        chapter = Chapters.objects.create(
            title=title,
            story=story,
            number=next_number,
            dictionary_completed=False,
        )

        Paragraphs.objects.bulk_create(
            Paragraphs(
                Chapter=chapter,
                number=i + 1,
                content=block,
            )
            for i, block in enumerate(paragraph_list)
        )

    return chapter
