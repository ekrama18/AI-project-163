"""Check the cleaned survey and the Q1 group calculations."""

import pandas as pd

from question1 import QUESTIONS, question_columns, rating_summary


def test_cleaned_survey():
    """Verify that renaming preserves survey responses and fixes Q1 labels."""
    original = pd.read_csv("responses.csv", low_memory=False)
    cleaned = pd.read_csv("cleaned_survey.csv", low_memory=False)

    assert "survey_language" in cleaned.columns
    headers = {}
    for header in cleaned.columns:
        code = header.split(" - ", 1)[0]
        headers[code] = header

    expected = {
        "Q13a": "Used chatbot: ChatGPT",
        "Q15": "To what extent do you use ChatGPT in general?",
        "Q26b": "improve my general knowledge.",
        "Q26c": "improve my specific knowledge.",
        "Q26e": "increase my study efficiency.",
    }
    for code in expected:
        assert expected[code] in headers[code]
        assert "Strongly disagree" not in headers[code]

    answers = question_columns(cleaned)
    assert answers.equals(original[QUESTIONS])
    cleaned.columns = original.columns
    assert cleaned.equals(original)


def test_rating_summary():
    """Check means, group sizes, and exclusion of incomplete responses."""
    answers = pd.DataFrame(
        [[1, 2, 3, 4], [1, 4, 5, 2], [5, 5, 4, 5], [5, 1, None, 1]],
        columns=QUESTIONS,
    )
    sizes, means = rating_summary(answers)
    assert sizes.loc[1] == 2
    assert sizes.loc[5] == 1
    assert sizes.loc[3] == 0
    assert means.loc[1].tolist() == [3.0, 4.0, 3.0]
    assert means.loc[5].tolist() == [5.0, 4.0, 5.0]


if __name__ == "__main__":
    test_cleaned_survey()
    test_rating_summary()
    print("Part 2 checks passed.")
