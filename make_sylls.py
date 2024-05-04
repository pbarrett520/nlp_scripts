from itertools import product
import re
import random


def join_tuple_strings(list_of_tuples: list[tuple[str, ...]]) -> list[tuple[str]]:
    return "".join(list_of_tuples)


def make_sylls(
    consonants: list[str],
    vowels: list[str],
    size: int,
    syll_struct_regex: str,
    seed: None | int,
) -> list[tuple[str]]:

    validation_set = set("bcdfghjklmnpqrstvwxyzaeiou")
    # vowels_validation_set = set("aeiou")

    if not consonants or not vowels:
        raise ValueError("Cannot perform operations on empty lists.")
    elif not set(consonants).issubset(validation_set) or not set(vowels).issubset(
        validation_set
    ):
        raise ValueError(
            "'consonants' and 'vowels' and  must be subsets of set('bcdfghjklmnpqrstvwxyz') and set('aeiou'), respectively."
        )

    syll_struct_regex = syll_struct_regex.lower()
    regex_validation_set = {char for char in syll_struct_regex if char.isalpha()}

    if not regex_validation_set.issubset(validation_set):
        raise ValueError(
            "Letters in regex must be a subset of set('bcdfghjklmnpqrstvwxyzaeiou')."
        )
    elif not syll_struct_regex or syll_struct_regex == " ":
        raise ValueError("syll_struct_regex must not be empty.")

    for element in [vowel.lower() for vowel in vowels] + [
        consonant.lower() for consonant in consonants
    ]:
        if not element:
            raise ValueError(
                "'Consonants' and/or 'vowels' cannot contain empty elements."
            )

    if seed is not None:
        random.seed(seed)
    else:
        seed = None

        syll_struct = re.compile(rf"{syll_struct_regex}")
        cartesian_product = product(consonants, vowels, consonants)

        sylls = list()

        for combination in cartesian_product:
            syll = join_tuple_strings(combination)

            if re.match(syll_struct, syll):
                sylls.append(syll)

        return sorted(random.sample(sylls, size))


# TEST
assert make_sylls(
    ["p", "t", "k"], ["a", "e", "i", "o", "u"], 5, "[p][aeiou][ptk]", seed=2
) == ["pap", "pat", "pok", "puk", "put"]
# TEST_END

# TEST
assert make_sylls(
    ["p", "t", "k"], ["a", "e", "i", "o", "u"], 5, "[ptk][aeiou][ptk]", seed=2
) == ["kup", "pek", "pep", "pot", "tik"]
# TEST_END

# TEST
assert make_sylls(
    ["p", "t", "k"], ["a", "e", "i", "o", "u"], 5, "[t][aeiou][t]", seed=2
) == ["tat", "tet", "tit", "tot", "tut"]
# TEST_END

# TEST
assert make_sylls(
    ["p", "t", "k"], ["a", "e", "i", "o", "u"], 5, "[t][aeiou][ptk]", seed=2
) == ["tap", "tat", "tok", "tuk", "tut"]
# TEST_END

# TEST
try:
    make_sylls(
        ["p", "t", "k"], ["a", "e", "i", "o", "u"], 90, "[t][aeiou][ptk]", seed=2
    )
    assert False

except ValueError as e:
    pass
# TEST_END

# TEST
try:
    make_sylls(
        ["p", "t", "k"], ["a", "e", "i", "o", "u"], -2, "[t][aeiou][ptk]", seed=2
    )
    assert False

except ValueError as e:
    pass
# TEST_END

# TEST
try:
    make_sylls([], [], 1, "[t][aeiou][ptk]", seed=2)
    assert False
except ValueError as e:
    pass
# TEST_END

# TEST
try:
    make_sylls([""], ["a"], 1, "[t][aeiou][ptk]", seed=2)
    assert False
except ValueError as e:
    pass
# TEST_END
