import re


def text_preprocess(frequent_words: set[str], text: str, normalize: bool) -> list[str]:

    if text == "":
        raise ValueError("Value 'text' must not be empty.")

    if frequent_words == {}:
        raise ValueError("Stop words set must not be empty.")

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split(" ")

    if normalize:
        cleaned_words = [
            word if word not in frequent_words else "<STOP>" for word in words
        ]
    else:
        cleaned_words = [word for word in words if word not in frequent_words]

    return cleaned_words


# TEST
assert text_preprocess({"is", "a", "the"}, "There is the snake in a boot", True) == [
    "there",
    "<STOP>",
    "<STOP>",
    "snake",
    "in",
    "<STOP>",
    "boot",
]
# TEST_END

# TEST
assert text_preprocess({"is", "a", "the"}, "There is the snake in a boot", False) == [
    "there",
    "snake",
    "in",
    "boot",
]
# TEST_END

# TEST
try:
    text_preprocess({}, "There is the snake in a boot", False)
    assert False
except ValueError as e:
    pass
# TEST_END

# TEST
try:
    text_preprocess({"is", "a", "the"}, "", False)
    assert False
except ValueError as e:
    pass
# TEST_END
