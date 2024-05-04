from collections import Counter
import re


def be_counter(sentence: str) -> list[(list[str], list[str]), Counter]:

    if sentence == "":
        raise ValueError("Cannot tokenize an empty string!")

    contraction_patterns = {
        re.compile(r"(who's|isn't|he's|she's|it's)"): "is",
        re.compile(r"(you're|they're|we're|aren't)"): "are",
        re.compile(r"(I'm)"): "am",
        re.compile(r"(wasn't)"): "was",
        re.compile(r"(weren't)"): "were",
    }

    copulas = {
        "am": "VBP",
        "is": "VBZ",
        "are": "VBP",
        "was": "VBD",
        "were": "VBD",
        "be": "VB",
        "being": "VBG",
        "been": "VBG",
    }

    sentence = sentence.lower()
    sentence = re.sub(r"[^\w\s']", "", sentence)
    sentence = sentence.split(" ")

    for i in range(len(sentence)):
        for pattern, replacement in contraction_patterns.items():
            if pattern.match(sentence[i]):
                sentence[i] = replacement

    just_copulas = [token for token in sentence if token in copulas.keys()]
    tags = [copulas[token] if token in copulas.keys() else "???" for token in sentence]
    counts = Counter(just_copulas + tags)

    return [(sentence, tags), counts]


# TEST
assert be_counter("Isn't") == [(["is"], ["VBZ"]), Counter({"is": 1, "VBZ": 1})]
# TEST

assert be_counter("Isn't, WAS") == [
    (["is", "was"], ["VBZ", "VBD"]),
    Counter({"is": 1, "was": 1, "VBZ": 1, "VBD": 1}),
]
# TEST

assert be_counter("My name is Jeff.") == [
    (["my", "name", "is", "jeff"], ["???", "???", "VBZ", "???"]),
    Counter({"???": 3, "is": 1, "VBZ": 1}),
]
# TEST

try:
    be_counter("")
except ValueError as e:
    assert str(e) == "Cannot tokenize an empty string!"
# TEST
