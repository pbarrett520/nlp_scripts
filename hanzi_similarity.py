def find_magnitude(vector: list[float]) -> float:

    return (sum(x * x for x in vector)) ** 0.5


def hanzi_similarity(
    decomposition1: dict[str, list[str]], decomposition2: dict[str, list[str]]
) -> float:

    stroke_encodings = {
        "冖": 1,
        "丶": 2,
        "㇛": 3,
        "一": 4,
        "丿": 5,
        "丨": 6,
        "八": 7,
        "丷": 8,
        "龶": 9,
        "冂": 10,
        "二": 11,
        "㇊": 12,
    }

    if not decomposition1 or not decomposition2:
        raise ValueError("Cannot perform operations on empty data entries.")

    stroke_vector1 = [
        stroke for sublist in decomposition1.values() for stroke in sublist
    ]
    stroke_vector2 = [
        stroke for sublist in decomposition2.values() for stroke in sublist
    ]

    for stroke in set((stroke_vector1 + stroke_vector2)):
        if stroke not in set(stroke_encodings.keys()):
            raise ValueError(f"Stroke '{stroke}' is not in the encodings table.")

    integer_vector1 = [stroke_encodings[stroke] for stroke in stroke_vector1]
    integer_vector2 = [stroke_encodings[stroke] for stroke in stroke_vector2]

    if not integer_vector1 or not integer_vector2:
        raise ValueError("Cannot compute cosine similarity of empty vector(s).")

    length_difference = abs(len(integer_vector1) - len(integer_vector2))
    if length_difference > 0:
        if len(integer_vector1) < len(integer_vector2):
            integer_vector1.extend([0] * length_difference)
        else:
            integer_vector2.extend([0] * length_difference)

    dot_product = sum(x * y for x, y in zip(integer_vector1, integer_vector2))
    cosine_similarity = dot_product / (
        find_magnitude(integer_vector1) * find_magnitude(integer_vector2)
    )

    return cosine_similarity


import math

# TEST
expected_result = 0.9320995887754049
result = hanzi_similarity(
    {"安": ["冖", "丶", "㇛", "一", "丿"]}, {"来": ["一", "丨", "八", "一", "丷"]}
)
assert math.isclose(result, expected_result)
# TEST_END

# TEST
expected_result = 0.6157666004701773
result = hanzi_similarity(
    {"请": ["㇊", "丶", "龶", "冂", "二"]}, {"青": ["龶", "冂", "二"]}
)
assert math.isclose(result, expected_result)
# TEST_END

# TEST
try:
    hanzi_similarity(
        {"请": ["㇊", "丶", "龶", "冂", "二"]}, {"青": ["龶", "冂", "二", "Q"]}
    )
    assert False
except ValueError as e:
    assert str(e) == "Stroke 'Q' is not in the encodings table."
# TEST_END

# TEST
try:
    hanzi_similarity(
        {"请": ["㇊", "丶", "龶", "冂", "二"]}, {"青": ["龶", "冂", "二", " "]}
    )
    assert False
except ValueError as e:
    assert str(e) == "Stroke ' ' is not in the encodings table."
# TEST_END


# TEST
try:
    hanzi_similarity({"请": ["㇊", "丶", "龶", "冂", "二"]}, {"青": []})
    assert False
except ValueError as e:
    assert str(e) == "Cannot compute cosine similarity of empty vector(s)."
# TEST_END

# TEST
try:
    hanzi_similarity({"青": []}, {"请": ["㇊", "丶", "龶", "冂", "二"]})
    assert False
except ValueError as e:
    assert str(e) == "Cannot compute cosine similarity of empty vector(s)."
# TEST_END

# TEST
try:
    hanzi_similarity({}, {})
    assert False
except ValueError as e:
    assert str(e) == "Cannot perform operations on empty data entries."
# TEST_END
