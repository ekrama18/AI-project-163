"""Explore perceived study benefits by extent of ChatGPT use."""

import matplotlib.pyplot as plt
import pandas as pd


USE = ["Rarely", "Occasionally", "Moderately", "Considerably", "Extensively"]
RATINGS = {
    "Q26b": "General knowledge",
    "Q26c": "Specific knowledge",
    "Q26e": "Study efficiency",
}
QUESTIONS = ["Q15", *RATINGS]
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
    fig, ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
    bars = ax.bar(USE, counts, color="#287488")
    ax.bar_label(bars, labels=[f"{n:,}" for n in counts], padding=3)
    ax.set(ylim=(0, counts.max() * 1.14), ylabel="Responses",
           xlabel="Extent of ChatGPT use (Q15)",
           title="How extensively students reported using ChatGPT")
    fig.savefig("q1_use.png", dpi=200)
    plt.close(fig)


def plot_ratings(means):
    """Save mean agreement for the three items by use level."""
    fig, ax = plt.subplots(figsize=(8, 3.8), layout="constrained")
    for code, color, marker in zip(RATINGS, ["#166778", "#922F44", "#946000"],
                                   ["o", "s", "^"]):
        ax.plot(USE, means[code], label=RATINGS[code],
                color=color, marker=marker, linewidth=2)
    ax.set(ylim=(1, 5), yticks=list(CODES), ylabel="Mean agreement (1–5)",
           xlabel="Extent of ChatGPT use (Q15)",
           title="Perceived study benefits by extent of ChatGPT use")
    ax.grid(axis="y", color="#dddddd")
    ax.legend(loc="lower right", ncol=3, frameon=False)
    fig.savefig("q1_ratings.png", dpi=200)
    plt.close(fig)


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
    print(means.assign(n=sizes)[["n", *RATINGS]].round(2).to_string())
    plot_usage(counts["Q15"])
    plot_ratings(means)


if __name__ == "__main__":
    main()
