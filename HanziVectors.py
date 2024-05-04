import json


class HanziVectors:

    def __init__(self) -> None:

        self.vocabulary = {}

        self.stroke_encodings = {
            "丶": 1,
            "一": 2,
            "丨": 3,
            "丿": 4,
            "乛": 5,
            "乚": 6,
            "𠃍": 7,
            "𠃌": 8,
            "㇀": 9,
            "㇁": 10,
            "㇂": 11,
            "㇃": 12,
            "㇄": 13,
            "㇅": 14,
            "㇇": 15,
            "㇈": 16,
            "㇉": 17,
            "㇊": 18,
            "㇋": 19,
            "㇌": 20,
            "㇍": 21,
            "㇎": 22,
            "㇏": 23,
            "㇐": 24,
            "㇑": 25,
            "㇚": 26,
            "㇛": 27,
            "冖": 28,
            "冂": 29,
            "八": 30,
            "丷": 31,
            "龶": 32,
            "二": 33,
        }

    def _magnitude(self, vector: list[float]) -> float:

        return (sum(x * x for x in vector)) ** 0.5

    def _extract_vectors(self, character: str) -> list[list[str], list[str]]:
        result = {}
        if character in self.vocabulary:
            data = self.vocabulary[character]
            if "decomposition" in data:
                vector_pairs = {}
                if "simplified" in data["decomposition"]:
                    vector_pairs["simplified"] = [
                        self.stroke_encodings.get(stroke, 0)
                        for stroke in data["decomposition"]["simplified"]
                    ]
                if "traditional" in data["decomposition"]:
                    vector_pairs["traditional"] = [
                        self.stroke_encodings.get(stroke, 0)
                        for stroke in data["decomposition"]["traditional"]
                    ]
                result = [
                    list(vector_pairs["simplified"]),
                    list(vector_pairs["traditional"]),
                ]
        return result

    def add_vocab(self, json_string: str) -> None:
        try:

            new_entry = json.loads(json_string)
            for key, value in new_entry.items():
                if key in self.vocabulary:
                    pass
                self.vocabulary[key] = value

        except json.JSONDecodeError as e:

            print(f"Error adding vocabulary: {str(e)}")

    def find_similarity(self, hanzi: str) -> float:

        if hanzi not in set(self.vocabulary.keys()):
            raise ValueError("Hanzi not in vocabulary.")

        vectors = self._extract_vectors(hanzi)

        integer_vector1 = vectors[0]
        integer_vector2 = vectors[1]

        if not integer_vector1 or not integer_vector2:
            raise ValueError("Cannot perform operations on empty data entries.")

        length_difference = abs(len(integer_vector1) - len(integer_vector2))

        if length_difference > 0:
            if len(integer_vector1) < len(integer_vector2):
                integer_vector1.extend([0] * length_difference)
            else:
                integer_vector2.extend([0] * length_difference)

        dot_product = sum(x * y for x, y in zip(integer_vector1, integer_vector2))
        cosine_similarity = dot_product / (
            self._magnitude(integer_vector1) * self._magnitude(integer_vector2)
        )

        return round(cosine_similarity, 2)


hanzi_vectors = HanziVectors()

qing = """
{
    "请": {
        "traditional": "請",
        "decomposition": {
            "simplified": ["㇊", "丶", "龶", "冂", "二"],
            "traditional": ["一", "丶", "二", "口", "龶", "冂", "二"]
        },
        "glosses": ["please", "invite", "treat"]
    }
}
"""
lai = """
{
    "来": {
        "traditional": "來",
        "decomposition": {
            "simplified": ["一", "丨", "八", "一", "丷"],
            "traditional": ["一", "丨", "八", "从"]
        },
        "glosses": ["come", "arrive", "future"]
    }
}
"""
# TEST
hanzi_vectors.add_vocab(
    """
{
    "请": {
        "traditional": "請",
        "decomposition": {
            "simplified": ["㇊", "丶", "龶", "冂", "二"],
            "traditional": ["一", "丶", "二", "口", "龶", "冂", "二"]
        },
        "glosses": ["please", "invite", "treat"]
    }
}
"""
)
hanzi_vectors.add_vocab(
    """
{
    "来": {
        "traditional": "來",
        "decomposition": {
            "simplified": ["一", "丨", "八", "一", "丷"],
            "traditional": ["一", "丨", "八", "从"]
        },
        "glosses": ["come", "arrive", "future"]
    }
}
"""
)

assert hanzi_vectors.vocabulary == {
    "请": {
        "traditional": "請",
        "decomposition": {
            "simplified": ["㇊", "丶", "龶", "冂", "二"],
            "traditional": ["一", "丶", "二", "口", "龶", "冂", "二"],
        },
        "glosses": ["please", "invite", "treat"],
    },
    "来": {
        "traditional": "來",
        "decomposition": {
            "simplified": ["一", "丨", "八", "一", "丷"],
            "traditional": ["一", "丨", "八", "从"],
        },
        "glosses": ["come", "arrive", "future"],
    },
}
# END TEST

# TEST
assert hanzi_vectors.find_similarity("来") == 0.7
# END TEST

# TEST
assert hanzi_vectors.find_similarity("请") == 0.59
# END TEST

# TEST
try:
    hanzi_vectors.find_similarity("f")
    assert False
except ValueError as e:
    assert str(e) == "Hanzi not in vocabulary."
#  END TEST

# TEST
try:
    hanzi_vectors.add_vocab("{asgfd}")
except json.JSONDecodeError as e:
    assert (
        str(e)
        == "Error adding vocabulary: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
    )
    assert False
# END TEST

# TEST
hanzi_vectors.add_vocab(
    """
{
    "高": {
        "traditional": "翠",
        "decomposition": {
            "simplified": [],
            "traditional": []
        },
        "glosses": ["please", "invite", "treat"]
    }
}
"""
)

try:
    hanzi_vectors.find_similarity("高")
    assert False
except ValueError as e:
    assert str(e) == "Cannot perform operations on empty data entries."
# END TEST
