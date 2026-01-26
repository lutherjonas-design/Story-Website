from django.test import TestCase
import re

# Create your tests here.

def _split_paragraphs(self, content: str) -> list[str]:
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
test_string = """Was waren die Träume der jungen Kadetten, als sie in die Akademie eintraten? Nun, je nach ihren Begabungen und Fähigkeiten waren diese Träume entsprechend unterschiedlich. Für Piloten standen diese Träume oft im Einklang mit dem Wunsch, brandneue Raptor-Kampfflugzeuge der Spitzenklasse zu fliegen – oft stellten sie sich vor, wie sie in die Schlacht flogen, um Ehre und Ruhm zu erlangen, wenn sich dank ihrer tapferen, heldenhaften Bemühungen das Blatt wendete.
Die Ehrgeizigeren träumten davon, in den Rängen aufzusteigen, um große Schiffe zu befehligen, sich mit allem zu umgeben, was eine solche Position mit sich brachte, und natürlich letztendlich Schlachtschiffe oder ganze Kampfgruppen oder eine der zehn Flotten in einer glorreichen Schlacht im Namen des Fürstentums zu befehligen.
Solche Träume waren nur Kadetten aus adligen Familien vorbehalten. Fern, aber auf die eine oder andere Weise erreichbar.
"""
test_string_2 = """First bit of text
asdasdasd
and a bit more 


lets see how this is handled."""

class ParagraphSplitTests(TestCase):
    def test_split_paragraphs(self,test_string):
        result = split_paragraphs(test_string)
        print(result)

test = ParagraphSplitTests()
print(test.test_split_paragraphs(test_string))
print(test.test_split_paragraphs(test_string_2))