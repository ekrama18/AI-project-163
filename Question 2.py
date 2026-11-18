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
    categorical_columns = ['Major_Category', 'Institutional_Policy', 'Burnout_Risk_Level',
                           'Q1', 'Q2', 'Q7', 'Q33', 'Q38', 'Q39', 'Q18a', 'Q18b', 'Q18c', 
                           'Q18d', 'Q18e', 'Q18f', 'Q18g', 'Q18h', 'Q18i', 'Q18j']
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


    graph_1 = sns.catplot(x='Major_Category', y='Weekly_GenAI_Hours', data=data[1], kind='bar', hue='Major_Category', height=6, aspect=1.5)
    graph_1.set_titles('AI Usage Time vs Study Consistency Index')
    graph_1.set_xlabels('Major Category')
    graph_1.set_ylabels('AI Usage Time (minutes)')
    graph_1.figure.savefig('ai_usage_vs_major.png')

    
    plt.tight_layout()
    graph_2 = sns.catplot(x='social_media_hours', y='ai_generated_content_percentage', data=data[0], height=6, aspect=1.5, kind = 'box')
    graph_2.set_titles('AI Usage Time vs Social Media Hours')
    graph_2.set_xlabels('Social Media Hours')
    graph_2.set_ylabels('AI Generated Content Percentage')
    graph_2.set_xticklabels(rotation=90)
    graph_2.figure.savefig('ai_usage_vs_social_media.png')

if __name__ == "__main__":
    main()