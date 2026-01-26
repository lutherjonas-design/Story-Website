# creates a list of words and symbols from a paragraph for the frontend
# This would be changed from:
#  Was waren die Träume der jungen Kadetten, als sie in die Akademie eintraten? 
#  to:
# [["Was", "waren", "die", "Träume", "der", "jungen", "Kadetten]", ",", ["als", "sie", "in", "die", "Akademie", "eintraten"], "?"]
def reformat_paragraph(content: str) -> list:
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
