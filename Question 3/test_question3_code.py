"""
Name: Jin Dai
Description of the program:
This program is to test functionality of the program in question3_code.py.
"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

import question3_code as q3

matplotlib.use("Agg")


def write_input_csvs(directory):
    """
    Write two sample CSVs and return their paths.
    """
    first_path = directory / "ai_student_impact_dataset (1).csv"
    second_path = directory / "ai_impact_student_performance_dataset.csv"

    pd.DataFrame({
        "Student_ID": [1, 2],
        "Year_of_Study": ["Freshman", "Senior"],
        "Pre_Semester_GPA": [2.0, 0.0],
        "Post_Semester_GPA": [2.5, 1.0],
        "Weekly_GenAI_Hours": [2, 3],
        "Traditional_Study_Hours": [6, 12],
        "Perceived_AI_Dependency": [2, 6],
    }).to_csv(first_path, index=False)

    pd.DataFrame({
        "student_id": [1],
        "grade_level": ["10th"],
        "study_hours_per_day": [2],
        "ai_dependency_score": [4],
        "improvement_rate": [12],
        "ai_generated_content_percentage": [25],
    }).to_csv(second_path, index=False)

    return first_path, second_path


class TestQuestion3Code(unittest.TestCase):
    def test_build_combined_dataset(self):
        """
        Check that both CSVs are combined into the expected dataset.
        """
        with tempfile.TemporaryDirectory() as directory:
            first, second = write_input_csvs(Path(directory))
            combined = q3.build_combined_dataset(first, second)

        expected = pd.DataFrame({
            "Grade_Improvement_Rate": [25.0, float("nan"), 12.0],
            "Est_AI_Dependency_Score": [2, 6, 4],
            "Grade_Level": ["1st Year", "4th Year", "10th"],
            "Traditional_Study_Hours_Per_Week": [6.0, 12.0, 10.5],
            "Weekly_AI_Study_Hours": [2.0, 3.0, 3.5],
            "Total_Study_Hour_Per_Week": [8.0, 15.0, 14.0],
        }, index=pd.Index([1, 2, 150001], name="Student_ID"))
        pd.testing.assert_frame_equal(combined, expected)

    def test_summarize_grade_improvement_groups_and_counts(self):
        """
        Check each group's mean improvement and count of valid scores.
        """
        combined = pd.DataFrame({
            "Grade_Level": ["1st Year"] * 5,
            "Total_Study_Hour_Per_Week": [0, 8, 9, 10, 10],
            "Est_AI_Dependency_Score": [0, 2, 2, 2, 4],
            "Grade_Improvement_Rate": [10.0, 20.0, float("nan"), 30.0, 40.0],
        })

        summary = q3.summarize_grade_improvement(combined)

        self.assertEqual(summary.to_dict(orient="index"), {
            ("1st Year", "0–<10", "0–2"): {
                "Mean_Grade_Improvement_Rate": 15.0, "Student_Count": 2,
            },
            ("1st Year", "10–<20", "0–2"): {
                "Mean_Grade_Improvement_Rate": 30.0, "Student_Count": 1,
            },
            ("1st Year", "10–<20", ">2–4"): {
                "Mean_Grade_Improvement_Rate": 40.0, "Student_Count": 1,
            },
        })

    def test_plot_grade_draws_the_selected_grade(self):
        """
        Check the selected grade's lines, labels, and plotted values.
        """
        summary = self.make_plot_summary()
        ax = Figure().subplots()
        colors = ["red", "green", "blue", "purple"]

        q3.plot_grade(ax, summary, "1st Year", colors)

        study_lines = ax.get_lines()[:-1]
        self.assertEqual(ax.get_title(), "1st Year")
        self.assertEqual(
            [line.get_label() for line in study_lines], q3.STUDY_HOUR_LABELS
        )
        self.assertEqual([line.get_color() for line in study_lines], colors)
        self.assertEqual(
            list(study_lines[0].get_xdata()), q3.DEPENDENCY_LABELS
        )
        self.assertEqual(study_lines[0].get_ydata()[0], 15.0)
        self.assertTrue(pd.isna(study_lines[0].get_ydata()[1]))
        self.assertEqual(list(ax.get_lines()[-1].get_ydata()), [0, 0])

    def test_plot_grade_improvement_returns_ordered_subplots(self):
        """
        Check that the visible grade subplots appear in order.
        """
        with matplotlib.rc_context():
            figure = q3.plot_grade_improvement(self.make_plot_summary())
        self.addCleanup(plt.close, figure)

        self.assertIsInstance(figure, Figure)
        visible_axes = [ax for ax in figure.axes if ax.get_visible()]
        self.assertEqual(
            [ax.get_title() for ax in visible_axes],
            ["1st Year", "Graduate", "Adult Learner"],
        )

    def test_main_writes_csv_and_grade_pngs(self):
        """
        Check that main writes the combined CSV and a PNG for each grade.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            write_input_csvs(directory)
            script_path = str(directory / "question3_code.py")
            with (
                matplotlib.rc_context(),
                patch.object(q3, "__file__", script_path),
                patch.object(q3.plt, "show", side_effect=plt.close) as show,
            ):
                q3.main()

            show.assert_called_once_with()
            combined = pd.read_csv(
                directory / "combined_student_impact_dataset.csv"
            )
            self.assertEqual(combined["Student_ID"].tolist(), [1, 2, 150001])
            pngs = list((directory / "grade_visualizations").glob("*.png"))
            self.assertEqual({path.name for path in pngs}, {
                "1st-year.png", "4th-year.png", "10th.png",
            })
            for path in pngs:
                with self.subTest(filename=path.name):
                    self.assertGreater(plt.imread(path).size, 0)

    @staticmethod
    def make_plot_summary():
        """
        Return sample grade improvement data for the plot tests.
        """
        index = pd.MultiIndex.from_tuples([
            ("1st Year", "0–<10", "0–2"),
            ("Adult Learner", "0–<10", "0–2"),
            ("Graduate", "0–<10", "0–2"),
        ], names=["Grade_Level", "Study_Hour_Range", "AI_Dependency_Range"])
        return pd.DataFrame(
            {"Mean_Grade_Improvement_Rate": [15.0, 30.0, 25.0]}, index=index
        )


if __name__ == "__main__":
    unittest.main()
