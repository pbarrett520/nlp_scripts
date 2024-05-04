import re


def named_entity_counter(text: str) -> dict[str:int] | str:

    NO_NAMED_ENTITIES = "No named entities found!"

    if text == "":
        raise ValueError("Value 'text' must not be empty.")

    named_entities = dict()
    PATTERN = re.compile(r"(?<!\.\s)(?!^)\b([A-Z]\w*(?:\s+[A-Z]\w*)*)")

    matches = re.findall(PATTERN, text)

    for match in matches:
        if match in named_entities:
            named_entities[match] += 1
        else:
            named_entities[match] = 1

    if "I" in named_entities.keys():
        named_entities.pop("I")

    if named_entities == {}:
        return NO_NAMED_ENTITIES
    else:
        return named_entities


# TEST
assert named_entity_counter(
    "My name is George Washington and I love the United States."
) == {"George Washington": 1, "United States": 1}

# TEST
assert named_entity_counter("The man pets the dog.") == "No named entities found!"

# TEST
try:
    named_entity_counter("")
except ValueError as e:
    assert str(e) == "Value 'text' must not be empty."
# TEST
