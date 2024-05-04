import re


def regex_conjugator(verb: str, person: int, number: str, voice: str) -> str:

    if not verb:
        raise ValueError("Cannot compute empty string value.")

    first_conj_end_validation = re.compile(r"([a-z]+are)")

    verb = verb.lower()

    if not re.search(first_conj_end_validation, verb):
        raise ValueError("Input must be a 1st conjugation infinitive verb.")

    vocabs = {
        "person_vocab": {1, 2, 3},
        "number_vocab": {"plural", "singular"},
        "voice_vocab": {"active", "passive"},
    }

    if person not in vocabs["person_vocab"]:
        raise ValueError(f"Valid inputs for 'person' are  '1', '2', or '3'.")
    elif number not in vocabs["number_vocab"]:
        raise ValueError("Valid inputs for 'number' are 'singular' or 'plural'.")
    elif voice not in vocabs["voice_vocab"]:
        raise ValueError("Valid inputs for 'voice' are 'active' or 'passive'.")

    conj_table = {
        "active": {
            "singular": {1: "o", 2: "as", 3: "at"},
            "plural": {1: "amus", 2: "atis", 3: "ant"},
        },
        "passive": {
            "singular": {1: "abar", 2: "abaris", 3: "abatur"},
            "plural": {1: "abamur", 2: "abamini", 3: "abantur"},
        },
    }

    return re.sub(r"are", conj_table[voice][number][person], verb)


# TEST
person_vocab = [1, 2, 3]
number_vocab = ["plural", "singular"]
voice_vocab = ["active", "passive"]

permutations = []
for person in person_vocab:
    for number in number_vocab:
        for voice in voice_vocab:

            permutations.append(regex_conjugator("amare", person, number, voice))

assert permutations == [
    "amamus",
    "amabamur",
    "amo",
    "amabar",
    "amatis",
    "amabamini",
    "amas",
    "amabaris",
    "amant",
    "amabantur",
    "amat",
    "amabatur",
]
# TEST END

# TEST
try:
    regex_conjugator("amare", 0, "active", "passive")
    assert False
except ValueError as e:
    assert str(e) == "Valid inputs for 'person' are  '1', '2', or '3'."
# END TEST

# TEST
try:
    regex_conjugator("are", 3, "active", "passive")
    assert False
except ValueError as e:
    assert str(e) == "Input must be a 1st conjugation infinitive verb."
# END TEST


# TEST
try:
    regex_conjugator("amare", 3, "jefgn", "passive")
    assert False
except ValueError as e:
    assert str(e) == "Valid inputs for 'number' are 'singular' or 'plural'."
# END TEST

# TEST
try:
    regex_conjugator("amare", 3, "singular", "jhfdsbg")
    assert False
except ValueError as e:
    assert str(e) == "Valid inputs for 'voice' are 'active' or 'passive'."
# END TEST

# TEST
try:
    regex_conjugator("", 3, "singular", "jhfdsbg")
    assert False
except ValueError as e:
    assert str(e) == "Cannot compute empty string value."
# END TEST
