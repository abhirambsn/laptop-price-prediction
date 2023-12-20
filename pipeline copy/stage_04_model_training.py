from pathlib import Path
import pandas as pd
import numpy as np
from joblib import dump
import logging, sys, os
from typing import List, Dict
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'model_training.log')
s_hnd = logging.StreamHandler(sys.stdout)

def adjusted_r2score(y_true, y_pred, n, p):
    r2 = r2_score(y_true, y_pred)
    return 1 - ((1 - r2) * (n - 1) / (n - p - 1))

class ModelTrainer:
    models: Dict[str, List]
    X_train: np.ndarray
    y_train: np.ndarray
    X_val: np.ndarray
    y_val: np.ndarray
    logger: logging.Logger
    best_model: object

    def __init__(self, models: Dict[str, List]):
        self.models = models
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)
        self.best_model = None
    
    def train(self):
        # Perform GridSearchCV for each model with its corresponding param_grid in list
        best_score = -1
        best_model = None
        best_model_name = None
        best_params = None

        for model_name, param_grid in self.models.items():
            self.logger.info(f"Training {model_name}...")
            model = GridSearchCV(param_grid=param_grid[1], estimator=param_grid[0], cv=5, n_jobs=-1, verbose=3)
            model.fit(self.X_train, self.y_train)
            self.logger.info(f"Best parameters for {model_name}: {model.best_params_}")
            self.logger.info(f"Best score for {model_name}: {model.best_score_}")
            if model.best_score_ > best_score:
                best_score = model.best_score_
                best_model = model
                best_model_name = model_name
                best_params = model.best_params_
                self.best_model = best_model

        self.logger.info(f"Best model: {best_model_name}")
        self.logger.info(f"Best score: {best_score}")
        self.logger.info(f"Best parameters: {best_params}")
        self.logger.info(f"Saving best model according to training...")
        dump(best_model, f"../models/best_model.joblib")
    
    def evaluate(self):
        # Evaluate model on validation set
        assert self.best_model is not None
        self.logger.info('Evaluating model on validation set...')
        y_pred = self.best_model.predict(self.X_val)
        mae = mean_absolute_error(self.y_val, y_pred)
        r2 = r2_score(self.y_val, y_pred)
        adj_r2 = adjusted_r2score(self.y_val, y_pred, len(self.X_val), len(self.X_val[0]))
        self.logger.info(f'Mean Absolute Error: {mae}')
        self.logger.info(f'R2: {r2}')
        self.logger.info(f"Adjusted R2: {adj_r2}")

        # Write evaluation metrics to file
        self.logger.info('Writing evaluation metrics to file...')
        timestamp = str(pd.Timestamp.now()).replace(' ', '_').replace(':', '-')
        with open(f'../reports/validation_metrics_{timestamp}.txt', 'w') as f:
            f.write(f'Mean Absolute Error: {mae}\n')
            f.write(f'R2: {r2}\n')
            f.write(f'Adjusted R2: {adj_r2}\n')
        self.logger.info('Model evaluation completed.')
    
    def main(self):
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 4: Model Training Started >>>>>>>>>>>>>>>>>')

        # Load Data
        self.X_train = np.load(Path(__file__).parent.parent / 'data/train.npy')
        self.y_train = self.X_train[:, -1]
        self.X_train = self.X_train[:, :-1]
        self.X_val = np.load(Path(__file__).parent.parent / 'data/val.npy')
        self.y_val = self.X_val[:, -1]
        self.X_val = self.X_val[:, :-1]

        # Train model
        self.train()

        # Evaluate model on validation set
        self.evaluate()
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 4: Model Training Completed >>>>>>>>>>>>>>>>>')
    