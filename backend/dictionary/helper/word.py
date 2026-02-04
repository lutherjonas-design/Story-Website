def syllable_list_to_breaks(syllables):
    """
    Return only the internal cut positions (strictly between 0 and len(word)).
    Example: ["hel", "lo"] -> [3]
             ["To", "ma", "ten"] -> [2, 4]
    """
    total = sum(len(s) for s in syllables)
    breaks = []
    pos = 0
    for s in syllables:
        pos += len(s)
        if pos < total:        # exclude the final edge
            breaks.append(pos)
    return breaks
