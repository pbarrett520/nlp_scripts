import re


def ngrams(text: str, window: int, eos_pos_tags: bool) -> list[tuple[str, ...]]:

    START_OF_SENTENCE = "</SOS>"
    END_OF_SENTENCE = "</EOS>"
    ngrams = []

    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()

    words = text.split(" ")

    if window > len(words):
        raise ValueError("Value 'n' exceeds length of the text.")

    if window == 0:
        raise ValueError("Value 'n' must be greater than 0.")

    if window < 0:
        raise ValueError("Value 'n' must be a positive integer.")

    if eos_pos_tags:
        words = [START_OF_SENTENCE] + words + [END_OF_SENTENCE]

    for word in range(len(words) - (window - 1)):
        ngrams.append(tuple(words[word : word + window]))

    return ngrams


# TEST
assert ngrams("In the beginning, God created the heavens and the Earth.", 2, True) == [
    ("</SOS>", "in"),
    ("in", "the"),
    ("the", "beginning"),
    ("beginning", "god"),
    ("god", "created"),
    ("created", "the"),
    ("the", "heavens"),
    ("heavens", "and"),
    ("and", "the"),
    ("the", "earth"),
    ("earth", "</EOS>"),
]
# TEST_END
# TEST
assert ngrams("In the beginning, God created the heavens and the Earth.", 2, False) == [
    ("in", "the"),
    ("the", "beginning"),
    ("beginning", "god"),
    ("god", "created"),
    ("created", "the"),
    ("the", "heavens"),
    ("heavens", "and"),
    ("and", "the"),
    ("the", "earth"),
]
# TEST_END
# TEST
assert ngrams("In the beginning, God created the heavens and the Earth.", 3, True) == [
    ("</SOS>", "in", "the"),
    ("in", "the", "beginning"),
    ("the", "beginning", "god"),
    ("beginning", "god", "created"),
    ("god", "created", "the"),
    ("created", "the", "heavens"),
    ("the", "heavens", "and"),
    ("heavens", "and", "the"),
    ("and", "the", "earth"),
    ("the", "earth", "</EOS>"),
]
# TEST_END
# TEST
ngrams("In the beginning, God created the heavens and the Earth.", 3, False) == [
    ("in", "the", "beginning"),
    ("the", "beginning", "God"),
    ("beginning", "god", "created"),
    ("god", "created", "the"),
    ("created", "the", "heavens"),
    ("the", "heavens", "and"),
    ("heavens", "and", "the"),
    ("and", "the", "earth"),
]
# TEST_END
# TEST
try:
    ngrams("In the beginning, God created the heavens and he Earth", 100, False)
except ValueError as e:
    assert str(e) == "Value 'n' exceeds length of the text."
# TEST_END
# TEST
try:
    ngrams("In the beginning, God created the heavens and he Earth", 0, False)
except ValueError as e:
    assert str(e) == "Value 'n' must be greater than 0."
# TEST_END
# TEST
try:
    ngrams("In the beginning, God created the heavens and he Earth", -1, False)
except ValueError as e:
    assert str(e) == "Value 'n' must be a positive integer."
# TEST_END

print(ngrams("", , True))
