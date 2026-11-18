from typing import Tuple

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


def get_size(data: pd.DataFrame) -> Tuple[int, int]:
    return data.shape


def contains_NaN(data: pd.DataFrame) -> bool:
    return data.isnull().values.any()

def percentage_of_NaN(data: pd.DataFrame) -> float:
    total_cells = data.size
    total_missing = data.isnull().sum().sum()
    return (total_missing / total_cells) * 100


def main():
    for dataset_number in [1, 2, 3]:
        data = get_data(dataset_number)
        size = get_size(data)
        has_nan = contains_NaN(data)

        print(f"Dataset {dataset_number}:")
        print(f"Size: {size}")
        print(f"Contains NaN values: {has_nan}")
        print(f"Percentage of NaN values: {percentage_of_NaN(data):.2f}%")
        print("-" * 30)


if __name__ == "__main__":
    main()
