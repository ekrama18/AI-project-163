"""Add PDF question text to survey column names and save one CSV.

Source: https://data.mendeley.com/datasets/nv2343nwsb/2 (CC BY 4.0).
Put questionnaire.pdf and responses.csv beside this script before running it.
"""

import re

import pandas as pd
from pypdf import PdfReader


def main():
    questions = {}
    options = []
    current = None

    for page in PdfReader("questionnaire.pdf").pages:
        for line in page.extract_text().splitlines():
            line = line.strip()
            if not line or line.startswith(("Global ChatGPT", "\u00a9", "SECTION")):
                continue
            code, _, wording = line.partition(" ")
            if re.fullmatch(r"Q\d+[a-z]?", code):
                current = code
                questions[code] = wording.removeprefix("-").strip()
            elif line.startswith("\u25a1"):
                options.append(line[1:].strip().rstrip(":"))
                current = None
            elif line.startswith(("o ", "(", "[", "Thank you")):
                current = None
            elif "Strongly disagree" in line or "Never Rarely" in line:
                if current:
                    stem = line.split("Strongly disagree")[0].split("Never Rarely")[0]
                    questions[current] += " " + stem.replace("\u2026", "").rstrip(". ")
                current = None
            elif current:
                questions[current] += " " + line

    # The six Q13 checkboxes have no individual question codes in the PDF.
    for letter, option in zip("abcdef", options):
        questions["Q13" + letter] = "Used chatbot: " + option
    questions["Q13f_text"] = "Other chatbot (written response)"

    data = pd.read_csv("responses.csv", low_memory=False)
    names = {"source": "survey_language"}
    for column in data.columns:
        if column.startswith("Q"):
            label = questions[column].strip()
            if re.fullmatch(r"Q\d+[a-z]", column) and not column.startswith("Q13"):
                label = questions[column[:-1]].strip() + " " + label
            names[column] = column + " - " + label

    data.rename(columns=names).to_csv("cleaned_survey.csv", index=False)


if __name__ == "__main__":
    main()
