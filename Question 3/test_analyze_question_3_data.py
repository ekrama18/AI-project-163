"""
Name: Jin Dai
Description of the program:
This program is to test functionality of the program in analyze_question3.py.
"""
import unittest

import pandas as pd

from analyze_question3_data import (
    get_data,
    get_dataset_dimensions,
    summarize_categorical,
    summarize_missing_data,
    summarize_numerical,
)


class TestAnalyzeQuestion3Data(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            "score": [10, 20, 30],
            "grade": ["Senior", "Senior", None],
        })

    def test_get_data_rejects_invalid_dataset(self):
        """
        Check that an invalid dataset number raises ValueError.
        """
        with self.assertRaises(ValueError):
            get_data(4)

    def test_get_dataset_dimensions(self):
        """
        Check that the dataset has three rows and two columns.
        """
        self.assertEqual(get_dataset_dimensions(self.data), (3, 2))

    def test_summarize_numerical(self):
        """
        Check the mean, sample standard deviation, and five-number summary.
        """
        expected = [20.0, 10.0, 10.0, 15.0, 20.0, 25.0, 30.0]
        self.assertEqual(summarize_numerical(self.data, "score"), expected)

    def test_summarize_categorical_ignores_missing_values(self):
        """
        Check that only the two non-missing grades are counted.
        """
        self.assertEqual(summarize_categorical(self.data, "grade"),
                         [("Senior", 2)])

    def test_summarize_missing_data_omits_complete_columns(self):
        """
        Check that only the grade column is reported as missing a value.
        """
        result = summarize_missing_data(self.data)
        self.assertEqual(result.to_dict(), {"grade": 1})


if __name__ == "__main__":
    unittest.main()
