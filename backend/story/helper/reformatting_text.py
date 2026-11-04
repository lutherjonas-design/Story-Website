# removes HTML tags and unescapes HTML entities from a string
def sanitize_text(value: str | None) -> str | None:
    from html import unescape
    from django.utils.html import strip_tags
    if value is None:
        return None
    return strip_tags(unescape(value)).strip()

# get all words of a given string, cannot be a list
def get_words(content: str) -> list:
    # NFC normalization for input needed
    char_test=lambda c: c.isalnum()
    L,i=0,0
    output=[]
    while i<len(content):
        if not char_test(content[i]):
            offset=1
            symbols = content[i]
            while i+offset<len(content) and not char_test(content[i+offset]):
                symbols += content[i+offset]
                offset+=1
            if len(symbols) > 1: # more logic for / etc
                output.extend(content[L:i].split(" "))
                i+=offset
                L=i
            else:
                i+=offset
        else:
            i+=1
    if L < len(content):
        if not char_test(content[-1]):
            output.extend(content[L:len(content)-1].split(" "))
        else:
            output.extend(content[L:].split(" "))
    return [word.lower() for word in output]

# creates a list of words and symbols from a paragraph for the frontend
# This would be changed from:
#  Was waren die Träume der jungen Kadetten, als sie in die Akademie eintraten? 
#  to:
# [["Was", "waren", "die", "Träume", "der", "jungen", "Kadetten]", ",", ["als", "sie", "in", "die", "Akademie", "eintraten"], "?"]
def reformat_text_output(content: str) -> list:
    # NFC normalization for input needed
    char_test=lambda c: c.isalnum()
    L,i=0,0
    output=[]
    while i<len(content):
        if not char_test(content[i]):
            offset=1
            symbols = content[i]
            while i+offset<len(content) and not char_test(content[i+offset]):
                symbols += content[i+offset]
                offset+=1
            if len(symbols) > 1: # more logic for / etc
                output.append(content[L:i].split(" "))
                output.append(symbols)
                i+=offset
                L=i
            else:
                i+=offset
        else:
            i+=1
    if L < len(content):
        if not char_test(content[-1]):
            output.append(content[L:len(content)-1].split(" "))
            output.append(content[-1])
        else:
            output.append(content[L:].split(" "))
    return output

def split_paragraphs(content: str) -> list[str]:
        import re
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