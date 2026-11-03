"""Feature order transcribed from the official SNAP data documentation.

Positions are one-based in the documentation and zero-based in Python.
LIWC values are lexical-category measurements, not psychological diagnoses.
"""

FEATURE_NAMES = [
    "n_characters", "n_characters_no_space", "fraction_letters", "fraction_digits",
    "fraction_uppercase", "fraction_spaces", "fraction_special", "n_words",
    "n_unique_words", "n_long_words", "mean_word_length", "n_unique_stopwords",
    "fraction_stopwords", "n_sentences", "n_long_sentences", "mean_sentence_characters",
    "mean_sentence_words", "readability_ari", "vader_positive", "vader_negative",
    "vader_compound",
] + ["liwc_" + name.lower() for name in [
    "Funct", "Pronoun", "Ppron", "I", "We", "You", "SheHe", "They", "Ipron",
    "Article", "Verbs", "AuxVb", "Past", "Present", "Future", "Adverbs", "Prep",
    "Conj", "Negate", "Quant", "Numbers", "Swear", "Social", "Family", "Friends",
    "Humans", "Affect", "Posemo", "Negemo", "Anx", "Anger", "Sad", "CogMech",
    "Insight", "Cause", "Discrep", "Tentat", "Certain", "Inhib", "Incl", "Excl",
    "Percept", "See", "Hear", "Feel", "Bio", "Body", "Health", "Sexual", "Ingest",
    "Relativ", "Motion", "Space", "Time", "Work", "Achiev", "Leisure", "Home",
    "Money", "Relig", "Death", "Assent", "Dissent", "Nonflu", "Filler",
]]
assert len(FEATURE_NAMES) == 86
