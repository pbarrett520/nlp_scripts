def conjugator(verb: str, person: int, singular: bool) -> str:

    if not verb:
        raise ValueError("Value 'verb' must not be empty.")

    verb = verb.lower()

    if verb[-3:] != "are" or len(verb) <= 3:
        raise ValueError("Input must be a 1st conjugation infinitive verb.")

    if person not in {1, 2, 3}:
        raise ValueError(f"'{person}' not a valid person number.")

    conj_table = {
        "singular": {1: "o", 2: "as", 3: "at"},
        "plural": {1: "amus", 2: "atis", 3: "ant"},
    }

    stem = verb[:-3]

    if singular:
        new_ending = conj_table["singular"][person]
    else:
        new_ending = conj_table["plural"][person]

    return stem + new_ending


# TEST
assert conjugator("amare", 1, True) == "amo"
# END TEST

# TEST
assert conjugator("amare", 2, True) == "amas"
# END TEST


# TEST
assert conjugator("amare", 3, True) == "amat"
# END TEST


# TEST
assert conjugator("amare", 1, False) == "amamus"
# END TEST


# TEST
assert conjugator("amare", 2, False) == "amatis"
# END TEST


# TEST
assert conjugator("amare", 3, False) == "amant"
# END TEST

# TEST
try:
    conjugator("amare", 0, False)
    assert False
except ValueError as e:
    pass
# END TEST

# TEST
try:
    conjugator("are", 3, False)
    assert False
except ValueError as e:
    pass
# END TEST

# TEST
try:
    conjugator("habere", 3, False)
    assert False
except ValueError as e:
    pass
# END TEST

# TEST
try:
    conjugator("", 3, False)
    assert False
except:
    pass
# END_TEST
