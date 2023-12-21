from joblib import load
import logging, sys, os, shutil
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'model_evaluation.log')
s_hnd = logging.StreamHandler(sys.stdout)

def adjusted_r2score(y_true, y_pred, n, p):
    r2 = r2_score(y_true, y_pred)
    return 1 - ((1 - r2) * (n - 1) / (n - p - 1))

class ModelEvaluator:
    model: object
    logger: logging.Logger
    X_test: np.ndarray
    y_test: np.ndarray

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)

        # Load Data
        self.X_test = np.load(Path(__file__).parent.parent / 'data/test.npy')
        self.y_test = self.X_test[:, -1]
        self.X_test = self.X_test[:, :-1]

        # Load Model
        self.model = load(Path(__file__).parent.parent / 'models/best_model.joblib')

    def evaluate(self):
        # Evaluate Model
        self.logger.info('Evaluating model...')
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        adj_r2 = adjusted_r2score(self.y_test, y_pred, len(self.X_test), len(self.X_test[0]))
        self.logger.info(f'Mean Absolute Error: {mae}')
        self.logger.info(f'R2: {r2}')
        self.logger.info(f'Adjusted R2: {adj_r2}')

        # Write evaluation metrics to file
        self.logger.info('Writing evaluation metrics to file...')
        timestamp = str(pd.Timestamp.now()).replace(' ', '_').replace(':', '-')
        with open(Path(__file__).parent.parent / f'reports/evaluation_metrics_{timestamp}.txt', 'w') as f:
            f.write(f'Mean Absolute Error: {mae}\n')
            f.write(f'R2: {r2}\n')
            f.write(f'Adjusted R2: {adj_r2}\n')
        self.logger.info('Model evaluation completed.')
    
    def copy_to_production(self):
        self.logger.info('Copying model to production...')
        shutil.copytree(Path(__file__).parent.parent / 'models', Path(__file__).parent.parent / 'app/models', symlinks=True, dirs_exist_ok=True)
        self.logger.info('Model copied to production.')
    
    def main(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 5: Model Evaluation Started >>>>>>>>>>>>>>>>>')
        self.evaluate()
        self.copy_to_production()
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 5: Model Evaluation Completed >>>>>>>>>>>>>>>>>')