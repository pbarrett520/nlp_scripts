def validate_character(character: str) -> bool:

    if len(character) != 1:
        raise ValueError("Input cannot exceed one character!")

    cjk_range = (0x4E00, 0x9FFF)
    code_point = ord(character)

    if cjk_range[0] <= code_point <= cjk_range[1]:
        return True
    else:
        raise ValueError("Input must be a Chinese character!")


# TEST
assert validate_character("个") == True

# TEST
assert validate_character("個") == True

# TEST
try:
    validate_character("I")
except ValueError as e:
    assert str(e) == "Input must be a Chinese character!"

# TEST
try:
    validate_character("き")
except ValueError as e:
    assert str(e) == "Input must be a Chinese character!"

# TEST
try:
    validate_character("한")
except ValueError as e:
    assert str(e) == "Input must be a Chinese character!"


# TEST
try:
    validate_character("ح")
except ValueError as e:
    assert str(e) == "Input must be a Chinese character!"

# TEST
try:
    validate_character("兄弟")
except ValueError as e:
    assert str(e) == "Input cannot exceed one character!"
# TEST
