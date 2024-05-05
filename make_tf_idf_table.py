from math import log
from collections import Counter


def tokenize(text: str) -> str:

    puncts = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

    no_punct = "".join([char.lower() if char not in puncts else " " for char in text])

    return no_punct.split()


def find_tf(tokenized_document: list[str]) -> dict[str, float]:

    tf_values = Counter(tokenized_document)

    total_words = len(tokenized_document)

    return {word: count / total_words for word, count in tf_values.items()}


def find_df(tokenized_corpus: list[list[str]]) -> dict[str, int]:

    df = Counter()

    for document in tokenized_corpus:
        unique_terms = set(document)
        df.update(unique_terms)

    return dict(df)


def make_tf_idf_table(corpus: list[tuple[int, str]]) -> list[dict[str, float]]:

    if not corpus:
        raise ValueError("Cannot perform operations on an empty corpus.")

    for doc in corpus:
        if not doc:
            raise ValueError("Corpus contains empty element(s).")

    tokenized_corpus = [tokenize(doc[1]) for doc in corpus]

    tfs = [find_tf(doc) for doc in tokenized_corpus]
    dfs = find_df(tokenized_corpus)
    corpus_length = len(tokenized_corpus)

    idfs = {word: log(corpus_length / frequency) for word, frequency in dfs.items()}

    tf_idf_table = [
        {word: tf[word] * idfs[word] for word in doc}
        for doc, tf in zip(tokenized_corpus, tfs)
    ]

    return tf_idf_table


from math import isclose

corpus = [
    (0, 'Jane said,"Look,look. I see a big yellow ear. See the yellow ear go.'),
    (
        1,
        'Sally said, "I see it. I see the big yellow ear. I want to go away in it. I want to go away, away."',
    ),
    (
        2,
        'Dick said, "Look up, Sally. You can see something. It is red and yellow. It can go up, up, up. It can go away."',
    ),
]


# TEST
assert make_tf_idf_table(corpus) == [
    {
        "jane": 0.07324081924454065,
        "said": 0.0,
        "look": 0.05406201441442192,
        "i": 0.02703100720721096,
        "see": 0.0,
        "a": 0.07324081924454065,
        "big": 0.02703100720721096,
        "yellow": 0.0,
        "ear": 0.05406201441442192,
        "the": 0.02703100720721096,
        "go": 0.0,
    },
    {
        "sally": 0.016894379504506847,
        "said": 0.0,
        "i": 0.06757751801802739,
        "see": 0.0,
        "it": 0.033788759009013694,
        "the": 0.016894379504506847,
        "big": 0.016894379504506847,
        "yellow": 0.0,
        "ear": 0.016894379504506847,
        "want": 0.0915510240556758,
        "to": 0.0915510240556758,
        "go": 0.0,
        "away": 0.05068313851352055,
        "in": 0.0457755120278379,
    },
    {
        "dick": 0.0457755120278379,
        "said": 0.0,
        "look": 0.016894379504506847,
        "up": 0.1831020481113516,
        "sally": 0.016894379504506847,
        "you": 0.0457755120278379,
        "can": 0.13732653608351372,
        "see": 0.0,
        "something": 0.0457755120278379,
        "it": 0.05068313851352055,
        "is": 0.0457755120278379,
        "red": 0.0457755120278379,
        "and": 0.0457755120278379,
        "yellow": 0.0,
        "go": 0.0,
        "away": 0.016894379504506847,
    },
]
# END TEST

# TEST
expected_output = [
    {
        "jane": 0.07324081924454065,
        "said": 0.0,
        "look": 0.05406201441442192,
        "i": 0.02703100720721096,
        "see": 0.0,
        "a": 0.07324081924454065,
        "big": 0.02703100720721096,
        "yellow": 0.0,
        "ear": 0.05406201441442192,
        "the": 0.02703100720721096,
        "go": 0.0,
    },
    {
        "sally": 0.016894379504506847,
        "said": 0.0,
        "i": 0.06757751801802739,
        "see": 0.0,
        "it": 0.033788759009013694,
        "the": 0.016894379504506847,
        "big": 0.016894379504506847,
        "yellow": 0.0,
        "ear": 0.016894379504506847,
        "want": 0.0915510240556758,
        "to": 0.0915510240556758,
        "go": 0.0,
        "away": 0.05068313851352055,
        "in": 0.0457755120278379,
    },
    {
        "dick": 0.0457755120278379,
        "said": 0.0,
        "look": 0.016894379504506847,
        "up": 0.1831020481113516,
        "sally": 0.016894379504506847,
        "you": 0.0457755120278379,
        "can": 0.13732653608351372,
        "see": 0.0,
        "something": 0.0457755120278379,
        "it": 0.05068313851352055,
        "is": 0.0457755120278379,
        "red": 0.0457755120278379,
        "and": 0.0457755120278379,
        "yellow": 0.0,
        "go": 0.0,
        "away": 0.016894379504506847,
    },
]


actual_output = make_tf_idf_table(corpus)
for doc_actual, doc_expected in zip(actual_output, expected_output):
    for word, expected_value in doc_expected.items():
        actual_value = doc_actual.get(word, 0)

        assert isclose(actual_value, expected_value)
# END TEST

# TEST
try:
    make_tf_idf_table([])
    assert False
except ValueError as e:
    assert str(e) == "Cannot perform operations on an empty corpus."
# END TEST

# TEST
try:
    make_tf_idf_table([["Hello"], []])
    assert False
except ValueError as e:
    assert str(e) == "Corpus contains empty element(s)."
# END TEST
