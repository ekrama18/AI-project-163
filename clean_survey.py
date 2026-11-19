"""Label the survey CSV using its questionnaire.

Source: https://data.mendeley.com/datasets/nv2343nwsb/2 (CC BY 4.0).
"""

import pandas as pd
from pypdf import PdfReader


def main():
    questions = {}
    choices = []
    current = None
    endings = ("o ", "(", "[", "Thank you", "Never Rarely")

    for page in PdfReader("questionnaire.pdf").pages:
        for line in page.extract_text().splitlines():
            line = line.strip()
            if not line or line.startswith(("Global ChatGPT", "©", "SECTION")):
                continue

            code, _, text = line.partition(" ")
            number = code[1:]
            if number and "a" <= number[-1] <= "z":
                number = number[:-1]

            if code.startswith("Q") and number.isdecimal():
                current = code
                questions[code] = text.removeprefix("-").strip()
            elif line.startswith("□"):
                choices.append(line[1:].strip().rstrip(":"))
                current = None
            elif line.startswith(endings):
                current = None
            elif current and "Strongly" in line:
                stem = line.split("Strongly", 1)[0].rstrip(" …")
                questions[current] += " " + stem
                current = None
            elif current:
                questions[current] += " " + line

    for letter, choice in zip("abcdef", choices):
        questions["Q13" + letter] = "Used chatbot: " + choice
    questions["Q13f_text"] = "Other chatbot (written response)"

    data = pd.read_csv("responses.csv", low_memory=False)
    names = {"source": "survey_language"}
    for code in data.columns:
        if code.startswith("Q"):
            label = questions[code].strip()
            if not code.startswith("Q13") and "a" <= code[-1] <= "z":
                label = questions[code[:-1]].strip() + " " + label
            names[code] = code + " - " + label

    data.rename(columns=names).to_csv("cleaned_survey.csv", index=False)


if __name__ == "__main__":
    main()
