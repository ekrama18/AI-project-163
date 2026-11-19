"""
Name: Jin Dai
Description of the program:
This program is used to analyze and explore data sets that are used for
Question 3 of the project.
"""
import pandas as pd

DATASET_1 = 'ai_impact_student_performance_dataset.csv'
DATASET_2 = 'ai_student_impact_dataset (1).csv'
DATASET_3 = 'combined_student_impact_dataset.csv'


def get_data(dataset) -> pd.DataFrame:
    """
    This program allows the client to get the corresponding pandas DataFrame
    for the data_set.
    """
    if dataset == 1:
        data = pd.read_csv(DATASET_1)
    elif dataset == 2:
        data = pd.read_csv(DATASET_2)
    elif dataset == 3:
        data = pd.read_csv(DATASET_3)
    else:
        raise ValueError("Invalid dataset number. Please choose 1, 2, or 3.")
    return data


def summarize_numerical(data: pd.DataFrame, column: str) -> list:
    """
    This program summarizes data from a specific column of the given dataframe
    numerically, the returned list is in a form of [mean, standard deviation,
    minimum value, first_quartile, third_quartile, maximum value]
    """
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataset.")

    mean = float(round(data[column].mean(), 2))
    median = float(round(data[column].median(), 2))
    std_dev = float(round(data[column].std(), 2))
    first_quartile = float(round(data[column].quantile(0.25), 2))
    third_quartile = float(round(data[column].quantile(0.75), 2))
    min_value = float(round(data[column].min(), 2))
    max_value = float(round(data[column].max(), 2))

    return [mean, std_dev, min_value, first_quartile, median, third_quartile,
            max_value]


def summarize_categorical(data: pd.DataFrame, column: str) -> list:
    """
    This method summarizes data from a specific column of the given dataframe
    categorically. It returns the list of tuples representing number of
    appereance for each value in the given column.
    """
    values = []
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataset.")

    for value in data[column].dropna().unique():
        count = data[data[column] == value].shape[0]
        values.append((str(value), count))
    return values


def get_dataset_dimensions(data: pd.DataFrame) -> tuple[int, int]:
    """
    This method returns the dimension of the given dataframe"
    """
    return data.shape


def summarize_missing_data(data: pd.DataFrame) -> pd.Series:
    """
    This method returns missing-value counts for columns with at least
    one missing value.
    """
    missing_counts = data.isna().sum()
    return missing_counts[missing_counts > 0]


def main():
    data = [get_data(1), get_data(2), get_data(3)]
    for filename, dataset in zip((DATASET_1, DATASET_2, DATASET_3), data):
        rows, columns = get_dataset_dimensions(dataset)
        print(f"{filename} has {rows:,} rows and {columns:,} columns.")
        missing_counts = summarize_missing_data(dataset)
        if missing_counts.empty:
            print(f"{filename} has no missing values.")
        else:
            print(f"{filename} has {missing_counts.sum()}" +
                  " missing values by column:")
            print(missing_counts.to_string())

    numerical_columns = ['Pre_Semester_GPA', 'Post_Semester_GPA',
                         'Weekly_GenAI_Hours', 'Traditional_Study_Hours',
                         'Perceived_AI_Dependency', 'study_hours_per_day',
                         'ai_dependency_score', 'improvement_rate',
                         'ai_generated_content_percentage',
                         'Grade_Improvement_Rate', 'Est_AI_Dependency_Score',
                         'Traditional_Study_Hours_Per_Week',
                         'Weekly_AI_Study_Hours', 'Total_Study_Hour_Per_Week']
    categorical_columns = ['Year_of_Study', 'grade_level', 'Grade_Level']
    for i in numerical_columns:
        for j in data:
            if i in j.columns:
                print(f"Summary statistics for {i}:")
                print(str(summarize_numerical(j, i)))
    for i in categorical_columns:
        for j in data:
            if i in j.columns:
                print(f"Summary statistics for {i}:")
                print(str(summarize_categorical(j, i)))


if __name__ == "__main__":
    main()
