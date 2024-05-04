def find_magnitude(vector: list[float]) -> float:

    return (sum(x * x for x in vector)) ** 0.5


def find_cosine_similarity(
    vector1: list[float], vector2: list[float], pad: bool
) -> float:

    if not vector1 or not vector2:
        raise ValueError("Cannot compute cosine similarity of empty vector(s).")

    if sum(vector1) + sum(vector2) == 0:
        raise ValueError(
            "Both vectors populated only by value '0', unable to divide zero by zero."
        )

    if pad:
        length_difference = abs(len(vector1) - len(vector2))
        if length_difference > 0:
            if len(vector1) < len(vector2):
                vector1.extend([0] * length_difference)
            else:
                vector2.extend([0] * length_difference)

    elif len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same length.")

    dot_product = sum(x * y for x, y in zip(vector1, vector2))
    cosine_similarity = dot_product / (
        find_magnitude(vector1) * find_magnitude(vector2)
    )

    return round(cosine_similarity, 2)


# TEST
assert find_cosine_similarity([1, 2, 1], [1, 1, 1], False) == 0.94
# TEST END

# TEST
assert find_cosine_similarity([1], [1, 1], True) == 0.71
# TEST END

# TEST
assert find_cosine_similarity([1, 1], [1], True) == 0.71
# TEST END

# TEST
try:
    find_cosine_similarity([1, 1], [1], False)
    assert False
except ValueError as e:
    assert str(e) == "Vectors must have the same length."
# TEST END

# TEST
try:
    find_cosine_similarity([], [1, 1, 1], True)
    assert False
except ValueError as e:
    assert str(e) == "Cannot compute cosine similarity of empty vector(s)."
# TEST END

# TEST
try:
    find_cosine_similarity([0], [0], False)
    assert False
except ValueError as e:
    assert (
        str(e)
        == "Both vectors populated only by value '0', unable to divide zero by zero."
    )
# TEST END
