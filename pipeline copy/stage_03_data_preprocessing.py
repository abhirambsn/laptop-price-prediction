from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

from pathlib import Path
import pandas as pd
import numpy as np
from joblib import dump
import logging, sys, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'data_preprocessing.log')
s_hnd = logging.StreamHandler(sys.stdout)

class DataPreprocessor:
    cleaned_path: Path
    dataset: pd.DataFrame
    logger: logging.Logger
    data_type: str

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data_type = data_path.suffix
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)

        if self.data_type == '.csv':
            self.dataset = pd.read_csv(data_path)
        elif self.data_type == '.json':
            self.dataset = pd.read_json(data_path)
        elif self.data_type == '.xlsx':
            self.dataset = pd.read_excel(data_path)
        else:
            raise Exception('Invalid file type')
    
    def main(self):
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 3: Data preprocessing Started >>>>>>>>>>>>>>>>>')
        X = self.dataset.drop('Price', axis=1)
        y = self.dataset['Price']

        numeric_features = X.select_dtypes(include=[np.number]).columns
        categorical_features = X.select_dtypes(include=['object']).columns

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OrdinalEncoder(), categorical_features)
            ]
        )

        X = preprocessor.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)
        np.save(Path(__file__).parent.parent / 'data/train.npy', np.concatenate((X_train, y_train.values.reshape(-1,1)), axis=1))
        np.save(Path(__file__).parent.parent / 'data/val.npy', np.concatenate((X_val, y_val.values.reshape(-1,1)), axis=1))
        np.save(Path(__file__).parent.parent / 'data/test.npy', np.concatenate((X_test, y_test.values.reshape(-1,1)), axis=1))
        dump(preprocessor, Path(__file__).parent.parent / 'models/preprocessor.joblib')
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 3: Data preprocessing Completed >>>>>>>>>>>>>>>>>')