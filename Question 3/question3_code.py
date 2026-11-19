"""
Name: Jin Dai
Description of the program:
This program is used to help answering Question 3 and getting visualizations
on the corresponding result.
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


USE_COL_DATA_1 = [
    "Student_ID", "Year_of_Study", "Pre_Semester_GPA", "Post_Semester_GPA",
    "Weekly_GenAI_Hours", "Traditional_Study_Hours", "Perceived_AI_Dependency",
]
USE_COL_DATA_2 = [
    "student_id", "grade_level", "study_hours_per_day",
    "ai_dependency_score", "improvement_rate",
    "ai_generated_content_percentage"
]

GRADE_ORDER = [
    "10th", "11th", "12th", "1st Year", "2nd Year", "3rd Year", "4th Year",
    "Graduate",
]
STUDY_HOUR_EDGES = [0, 10, 20, 30, float("inf")]
STUDY_HOUR_LABELS = ["0–<10", "10–<20", "20–<30", "30+"]
DEPENDENCY_EDGES = [0, 2, 4, 6, 8, 10]
DEPENDENCY_LABELS = ["0–2", ">2–4", ">4–6", ">6–8", ">8–10"]


def build_combined_dataset(dataset1, dataset2) -> pd.DataFrame:
    """
    This method combines dataset1 and dataset2 according to the instructions
    described in the report for solving Question3.
    """
    first = pd.read_csv(dataset1,
                        usecols=USE_COL_DATA_1).set_index("Student_ID")
    second = pd.read_csv(dataset2,
                         usecols=USE_COL_DATA_2).set_index("student_id")
    second.index = (second.index + 150000).rename("Student_ID")

    grade_mapping = {
        "Freshman": "1st Year",
        "Sophomore": "2nd Year",
        "Junior": "3rd Year",
        "Senior": "4th Year",
    }

    # Percentage change is undefined when the starting GPA is zero.
    starting_gpa = first["Pre_Semester_GPA"]
    gpa_change = first["Post_Semester_GPA"] - starting_gpa
    first_combined = pd.DataFrame({
        "Grade_Improvement_Rate": (
            gpa_change.div(starting_gpa.where(starting_gpa != 0)) * 100
        ),
        "Est_AI_Dependency_Score": first["Perceived_AI_Dependency"],
        "Grade_Level": first["Year_of_Study"].replace(grade_mapping),
        "Traditional_Study_Hours_Per_Week": first["Traditional_Study_Hours"],
        "Weekly_AI_Study_Hours": first["Weekly_GenAI_Hours"],
    })

    weekly_hours = 7 * second["study_hours_per_day"]
    # Apply the requested content-based estimate to all Dataset 2 rows.
    ai_share = second["ai_generated_content_percentage"] / 100
    second_combined = pd.DataFrame({
        "Grade_Improvement_Rate": second["improvement_rate"],
        "Est_AI_Dependency_Score": second["ai_dependency_score"],
        "Grade_Level": second["grade_level"],
        "Traditional_Study_Hours_Per_Week": weekly_hours * (1 - ai_share),
        "Weekly_AI_Study_Hours": weekly_hours * ai_share,
    })

    combined = pd.concat([first_combined, second_combined],
                         verify_integrity=True)
    combined["Total_Study_Hour_Per_Week"] = (
        combined["Traditional_Study_Hours_Per_Week"] +
        combined["Weekly_AI_Study_Hours"]
    )
    return combined


def summarize_grade_improvement(combined: pd.DataFrame) -> pd.DataFrame:
    """
    This method summarizes the grade improvement of each student in the
    combined dataset, and categorized the data by students' grade levels
    , study times, and AI dependency levels.
    """
    study_range = pd.cut(
        combined["Total_Study_Hour_Per_Week"],
        bins=STUDY_HOUR_EDGES,
        labels=STUDY_HOUR_LABELS,
        right=False,
    ).rename("Study_Hour_Range")
    dependency_range = pd.cut(
        combined["Est_AI_Dependency_Score"],
        bins=DEPENDENCY_EDGES,
        labels=DEPENDENCY_LABELS,
        include_lowest=True,
    ).rename("AI_Dependency_Range")

    return combined.groupby(
        ["Grade_Level", study_range, dependency_range], observed=True
    )["Grade_Improvement_Rate"].agg(
        Mean_Grade_Improvement_Rate="mean",
        Student_Count="count",
    )


def plot_grade(ax, summary: pd.DataFrame, grade: str, colors):
    """
    This method plots the grade graph for the given grade level.
    """
    means = summary.loc[grade, "Mean_Grade_Improvement_Rate"] \
        .unstack("Study_Hour_Range")
    means = means.reindex(index=DEPENDENCY_LABELS, columns=STUDY_HOUR_LABELS)
    for hour_range, color in zip(STUDY_HOUR_LABELS, colors):
        ax.plot(DEPENDENCY_LABELS, means[hour_range], marker="o",
                color=color, label=hour_range)
    ax.axhline(0, color="0.5", linewidth=0.8)
    ax.set_title(grade)


def plot_grade_improvement(summary, output_directory=None):
    """
    This method returns one Matplotlib figure with a subplot for each
    grade level.
    """
    sns.set_theme(style="whitegrid")
    grades = summary.index.get_level_values("Grade_Level").unique()
    grades = sorted(grades, key=lambda grade: (
        GRADE_ORDER.index(grade) if grade in GRADE_ORDER
        else len(GRADE_ORDER),
        grade))
    columns = 4
    rows = (len(grades) + columns - 1) // columns
    fig, axes = plt.subplots(
        rows, columns, figsize=(14, 3.3 * rows + 1),
        sharex=True, sharey=True, squeeze=False,
    )

    colors = sns.color_palette("colorblind", n_colors=len(STUDY_HOUR_LABELS))
    for ax, grade in zip(axes.flat, grades):
        plot_grade(ax, summary, grade, colors)
        ax.tick_params(axis="x", labelbottom=True)

    for ax in list(axes.flat)[len(grades):]:
        ax.set_visible(False)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, title="Total study hours per week",
               loc="upper center", bbox_to_anchor=(0.5, 0.94),
               ncol=len(labels))
    fig.suptitle("Grade improvement by estimated AI dependency")
    fig.supxlabel("Estimated AI dependency score")
    fig.supylabel("Mean grade improvement rate (%)")
    fig.tight_layout(rect=(0.02, 0.03, 1, 0.84))

    if output_directory is not None:
        output_directory.mkdir(parents=True, exist_ok=True)
        y_limits = axes[0, 0].get_ylim()
        for grade in grades:
            grade_fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
            plot_grade(ax, summary, grade, colors)
            ax.set(xlabel="Estimated AI dependency score",
                   ylabel="Mean grade improvement rate (%)", ylim=y_limits)
            grade_fig.suptitle("Grade improvement by estimated AI dependency")
            grade_fig.legend(title="Total study hours per week",
                             ncol=len(STUDY_HOUR_LABELS),
                             loc="outside lower center")
            filename = f"{grade.lower().replace(' ', '-')}.png"
            grade_fig.savefig(output_directory / filename, dpi=200)
            plt.close(grade_fig)

    return fig


def main():
    # Use the script's folder even when the terminal is in a different folder.
    script_directory = Path(__file__).resolve().parent
    combined = build_combined_dataset(
        script_directory / 'ai_student_impact_dataset (1).csv',
        script_directory / "ai_impact_student_performance_dataset.csv",
    )
    combined.to_csv(script_directory / "combined_student_impact_dataset.csv")
    summary = summarize_grade_improvement(combined)
    plot_grade_improvement(summary, script_directory / "grade_visualizations")
    plt.show()


if __name__ == "__main__":
    main()
