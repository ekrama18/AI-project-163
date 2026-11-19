"""Explore perceived study benefits by extent of ChatGPT use."""

import matplotlib.pyplot as plt
import pandas as pd


USE = ["Rarely", "Occasionally", "Moderately", "Considerably", "Extensively"]
RATINGS = {
    "Q26b": "General knowledge",
    "Q26c": "Specific knowledge",
    "Q26e": "Study efficiency",
}
QUESTIONS = ["Q15", "Q26b", "Q26c", "Q26e"]
CODES = range(1, 6)


def question_columns(survey):
    """Select the four questions using the codes in the cleaned headers."""
    codes = [name.split(" - ", 1)[0] for name in survey.columns]
    return survey.set_axis(codes, axis=1)[QUESTIONS]


def rating_summary(answers):
    """Return the complete-case group sizes and mean ratings by use level."""
    groups = answers.dropna().groupby("Q15")
    sizes = groups.size().reindex(CODES, fill_value=0)
    means = groups.mean().reindex(CODES)
    return sizes, means


def plot_usage(counts):
    """Save the distribution of answers to Q15."""
    plt.figure(figsize=(8, 4))
    plt.bar(USE, counts)
    plt.xlabel("Extent of ChatGPT use (Q15)")
    plt.ylabel("Responses")
    plt.title("How extensively students reported using ChatGPT")
    plt.tight_layout()
    plt.savefig("q1_use.png", dpi=200)
    plt.close()


def plot_ratings(means):
    """Save mean agreement for the three items by use level."""
    plt.figure(figsize=(8, 4))
    for code in RATINGS:
        plt.plot(USE, means[code], marker="o", label=RATINGS[code])
    plt.ylim(1, 5)
    plt.yticks(CODES)
    plt.xlabel("Extent of ChatGPT use (Q15)")
    plt.ylabel("Mean agreement (1–5)")
    plt.title("Perceived study benefits by extent of ChatGPT use")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("q1_ratings.png", dpi=200)
    plt.close()


def main():
    """Print the EDA tables and write both figures."""
    survey = pd.read_csv("cleaned_survey.csv", low_memory=False)
    answers = question_columns(survey)
    missing = answers.isna().sum()
    counts = pd.DataFrame({
        code: answers[code].value_counts().reindex(CODES, fill_value=0)
        for code in QUESTIONS
    })
    sizes, means = rating_summary(answers)

    print("Survey rows and columns:", survey.shape)
    print("Missing cells overall:", survey.isna().sum().sum())
    print("\nCounts by response code:")
    print(counts.to_string())
    print("\nMissing by question:")
    print(pd.DataFrame({
        "count": missing, "percent": (100 * missing / len(survey)).round(2)
    }).to_string())
    print("\nComplete-case group sizes and mean ratings:")
    means.insert(0, "n", sizes)
    print(means.round(2).to_string())
    plot_usage(counts["Q15"])
    plot_ratings(means)


if __name__ == "__main__":
    main()
