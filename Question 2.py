import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATASET_1 = 'ai_impact_student_performance_dataset.csv'
DATASET_2 = 'ai_student_impact_dataset (1).csv'
DATASET_3 = 'final dataset.csv'


def get_data(dataset) -> pd.DataFrame:
    if dataset == 1:
        data = pd.read_csv(DATASET_1)
    elif dataset == 2:
        data = pd.read_csv(DATASET_2)
    elif dataset == 3:
        data = pd.read_csv(DATASET_3, encoding='utf-8')
    else:
        raise ValueError(
            "Invalid dataset number. Please choose 1, 2, or 3."
        )
    return data


def summarize_numerical(data: pd.DataFrame, column: str) -> list:
    if column not in data.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    mean = float(round(data[column].mean(), 2))
    median = float(round(data[column].median(), 2))
    std_dev = float(round(data[column].std(), 2))
    first_quartile = float(round(data[column].quantile(0.25), 2))
    third_quartile = float(round(data[column].quantile(0.75), 2))
    min_value = float(round(data[column].min(), 2))
    max_value = float(round(data[column].max(), 2))

    return [
        mean,
        std_dev,
        min_value,
        first_quartile,
        median,
        third_quartile,
        max_value
    ]


def test_summarize_numerical( file_path: str, column: str,
                             expected_summary: list
                             ):
    data = pd.read_csv(file_path)
    assert summarize_numerical(data, column) == expected_summary


def summarize_categorical(data: pd.DataFrame, column: str) -> list:
    values = []

    if column not in data.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    for value in data[column].dropna().unique():
        count = data[data[column] == value].shape[0]
        values.append((str(value), count))

    return values


def test_summarize_categorical(file_path: str, column: str, 
                               expected_summary: list
                               ):
    data = pd.read_csv(file_path)
    assert summarize_categorical(data, column) == expected_summary


def main():
    data = [get_data(1), get_data(2), get_data(3)]

    numerical_columns = [
        'attendance_percentage',
        'study_consistency_index',
        'sleep_hours',
        'social_media_hours',
        'class_participation_score',
        'ai_usage_time_minutes',
        'Traditional_Study_Hours',
        'Anxiety_Level_During_Exams',
        'Weekly_GenAI_Hours'
    ]

    categorical_columns = [
        'Major_Category',
        'Institutional_Policy',
        'Burnout_Risk_Level',
        'gender'
    ]

    for i in numerical_columns:
        for j in data:
            if i in j.columns:
                print(f"Summary statistics for " + i + ":")
                print(str(summarize_numerical(j, i)))

    for i in categorical_columns:
        for j in data:
            if i in j.columns:
                print(f"Summary statistics for " + i + ":")
                print(str(summarize_categorical(j, i)))

    graph_1 = sns.catplot(
        x='Major_Category',
        y='Weekly_GenAI_Hours',
        data=data[1],
        kind='bar',
        hue='Major_Category',
        height=6,
        aspect=1.5
    )
    graph_1.fig.subplots_adjust(top=0.88)
    graph_1.fig.suptitle('AI Usage Time vs Major Category', fontsize=16)
    graph_1.set_xlabels('Major Category')
    graph_1.set_ylabels('AI Usage Time (minutes)')
    graph_1.figure.savefig('ai_usage_vs_major.png')

    graph_2 = sns.catplot(
        x='social_media_hours',
        y='ai_generated_content_percentage',
        data=data[0],
        height=6,
        aspect=1.5,
        kind='box'
    )
    graph_2.fig.subplots_adjust(top=0.88)
    graph_2.fig.suptitle(
    'AI-Generated Content vs Social Media Hours',
    fontsize=16
    )
    graph_2.set_xlabels('Social Media Hours')
    graph_2.set_ylabels('AI Generated Content Percentage')
    graph_2.set_xticklabels(rotation=90)
    graph_2.figure.savefig('ai_usage_vs_social_media.png')

    test_summarize_numerical(
        'test_mixed_data.csv',
        'Age',
        [
            28.38,
            7.17,
            19.0,
            23.5,
            27.5,
            32.0,
            41.0
        ]
    )

    test_summarize_categorical(
        'test_mixed_data.csv',
        'Major',
        [
            ('Engineering', 2),
            ('Biology', 2),
            ('History', 2),
            ('Business', 1),
            ('Computer Science', 1)
        ]
    )

    test_summarize_numerical(
        'test_mixed_data_20x5.csv',
        'Weekly_Study_Hours',
        [14.0, 5.68, 5.0, 9.75, 13.5, 18.25, 25.0]
    )

    test_summarize_categorical(
        'test_mixed_data_20x5.csv',
        'Study_Preference',
        [
            ('Group', 7),
            ('Independent', 7),
            ('Tutoring', 6)
        ]
    )


if __name__ == "__main__":
    main()