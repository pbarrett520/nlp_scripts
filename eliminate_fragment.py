def eliminate_fragment(llm_output: str) -> str:

    if llm_output == "":
        raise ValueError("Cannot perform operations on empty string")

    character_set = {*llm_output}

    if (
        "." not in character_set
        and '"' not in character_set
        and "?" not in character_set
        and "!" not in character_set
    ):
        raise ValueError("No sentence ending punctuation detected.")

    period = llm_output.rfind(".")
    question_mark = llm_output.rfind("?")
    exclamation_mark = llm_output.rfind("!")
    quote = llm_output.rfind('"')

    if period > question_mark and period > exclamation_mark and period > quote:
        return llm_output[: period + 1]

    elif (
        question_mark > period
        and question_mark > exclamation_mark
        and question_mark > quote
    ):
        return llm_output[: question_mark + 1]

    elif (
        exclamation_mark > period
        and exclamation_mark > question_mark
        and exclamation_mark > quote
    ):
        return llm_output[: exclamation_mark + 1]

    else:
        return llm_output[: quote + 1]


# TEST
assert eliminate_fragment('Test. Test! Test? Test" Test') == 'Test. Test! Test? Test"'
# END TEST

# TEST
assert eliminate_fragment('Test. Test! Test" Test? Test') == 'Test. Test! Test" Test?'
# END TEST

# TEST
assert eliminate_fragment('Test. Test" Test? Test! Test') == 'Test. Test" Test? Test!'
# END TEST

# TEST
assert eliminate_fragment('Test" Test! Test? Test. Test') == 'Test" Test! Test? Test.'
# END TEST

# TEST
assert eliminate_fragment('Test" Test. Test') == 'Test" Test.'
# END TEST

# TEST
try:
    eliminate_fragment("Test")
except ValueError as e:
    assert str(e) == "No sentence ending punctuation detected."
# END TEST

# TEST
try:
    eliminate_fragment("")
except ValueError as e:
    assert str(e) == "Cannot perform operations on empty string"
# END TEST
