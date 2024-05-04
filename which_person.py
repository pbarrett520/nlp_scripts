def which_person(text: str, confidence_threshold: float) -> tuple[bool, float]:

    if confidence_threshold > 1 or confidence_threshold < 0:
        raise ValueError("Confidence threshold must be between 0 and 1.")
    elif text == "":
        raise ValueError("String 'text' must not be empty.")

    if text == "":
        raise ValueError("Cannot perform operations on empty string.")

    first_person = {
        "i",
        "me",
        "my",
        "mine",
        "myself",
        "we",
        "us",
        "our",
        "ours",
        "ourselves",
        "i'm",
        "we're",
    }

    third_person = {
        "he",
        "him",
        "his",
        "himself",
        "she",
        "her",
        "hers",
        "herself",
        "it",
        "its",
        "itself",
        "they",
        "them",
        "their",
        "theirs",
        "themself",
        "themselves",
        "he's",
        "she's",
        "it's",
        "they're",
    }

    text = text.lower()
    text = text.split(" ")

    first_person_counter = 0
    third_person_counter = 0

    for word in text:

        if word in first_person:
            first_person_counter += 1
        elif word in third_person:
            third_person_counter += 1

    if first_person_counter == 0 and third_person_counter == 0:
        first_person_prob = 0
    elif third_person_counter == 0:
        first_person_prob = 1
    else:
        first_person_prob = round(first_person_counter / third_person_counter, 3)

    if first_person_prob >= confidence_threshold:
        decision = True
    else:
        decision = False

    return (decision, first_person_prob)


import math

# TEST
decision, probability = which_person(
    "I I me we us he he her hers hers himself",
    0.5,
)
assert decision == True
assert math.isclose(probability, 0.833)
# END_TEST

# TEST
decision, probability = which_person(
    "I I me we us he he her hers hers himself",
    0.9,
)
assert decision == False
assert math.isclose(probability, 0.833)
# END_TEST

# TEST
decision, probability = which_person(
    "he he her hers hers himself",
    0.1,
)
assert decision == False
assert math.isclose(probability, 0)
# END_TEST

# TEST
decision, probability = which_person(
    "Hello World",
    0.55,
)
assert decision == False
assert math.isclose(probability, 0)
# END_TEST

# TEST
try:
    decision, probability = which_person(
        "I he he",
        -0.55,
    )
except ValueError as e:
    assert str(e) == "Confidence threshold must be between 0 and 1."
# END_TEST

# TEST
try:
    decision, probability = which_person(
        "",
        0.55,
    )
except ValueError as e:
    assert str(e) == "String 'text' must not be empty."
# END_TEST
