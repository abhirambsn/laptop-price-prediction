from stage_01_data_ingestion import DataIngestion
from stage_02_data_cleaner import DataCleaner
from stage_03_data_preprocessing import DataPreprocessor
from stage_04_model_training import ModelTrainer
from stage_05_model_evaluation import ModelEvaluator

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from pathlib import Path

def main():
    print('Pipeline started...')
    data_cleaning = DataCleaner(data_path=Path(__file__).parent.parent / "data/dataset_raw.csv")
    data_cleaning.main()

    data_preprocessing = DataPreprocessor(data_path=Path(__file__).parent.parent / "data/dataset_cleaned.csv")
    data_preprocessing.main()

    model_training = ModelTrainer(models={
        'DecisionTreeRegressor': [DecisionTreeRegressor(random_state=42), {
                'criterion': ['absolute_error'],
                'splitter': ['best', 'random'],
                'max_depth': [4, 5, 6, 7, 8],
                'min_samples_split': [2, 3, 4, 5],
                'min_samples_leaf': [1, 2, 3, 4, 5],
                'max_features': ['sqrt', 'log2']
        }],
        'LinearRegression': [LinearRegression(), {
                'fit_intercept': [True, False],
                'copy_X': [True, False]
        }],
        'RandomForestRegressor': [RandomForestRegressor(random_state=42), {
                'n_estimators': [100, 200, 300, 400, 500],
                'max_features': ['sqrt', 'log2'],
                'max_depth': [4, 5, 6, 7, 8],
                'criterion': ['absolute_error']
        }]
    })
    model_training.main()

    model_evaluation = ModelEvaluator()
    model_evaluation.main()

    print('Pipeline completed.')

if __name__ == '__main__':
      main()