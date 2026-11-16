import matplotlib.pyplot as plt
import pandas as pd

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
        raise ValueError("Invalid dataset number. Please choose 1, 2, or 3.")
    return data

def summarize_numerical(data: pd.DataFrame, column: str) -> list:
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataset.")
    
    mean = float(round(data[column].mean(), 2))
    median = float(round(data[column].median(), 2))
    std_dev = float(round(data[column].std(), 2))
    first_quartile = float(round(data[column].quantile(0.25), 2))
    third_quartile = float(round(data[column].quantile(0.75), 2))
    min_value = float(round(data[column].min(), 2))
    max_value = float(round(data[column].max(), 2))

    return [mean, std_dev, min_value, first_quartile, median, third_quartile, max_value]

def summarize_categorical(data: pd.DataFrame, column: str) -> list:
    values = []
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataset.")
    
    for value in data[column].dropna().unique():
        count = data[data[column] == value].shape[0]
        values.append((str(value), count))
    return values

def main():
    data = [get_data(1), get_data(2), get_data(3)]
    numerical_columns = ['attendance_percentage', 'study_consistency_index',
                         'sleep_hours', 'social_media_hours', 
                         'class_participation_score', 'ai_usage_time_minutes'
                         'Traditional_Study_Hours', 'Anxiety_Level_During_Exams',
                         'Weekly_GenAI_Hours']
    categorical_columns = ['Major_Category', 'Institutional_Policy', 'Burnout_Risk_Level'
                           'Q1', 'Q2', 'Q7', 'Q33', 'Q38', 'Q39', 'Q18']
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
    
if __name__ == "__main__":
    main()