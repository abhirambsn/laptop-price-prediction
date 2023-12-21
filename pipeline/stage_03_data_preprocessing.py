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

def categorize_screen_resolution(res_X, res_Y):
    resolution_mapping = {
        'HD': ['1366x768', '1280x720'],
        'FHD': ['1920x1080'],
        '2k': ['2560x1440'],
        '4k': ['3840x2160'],
        '8': ['7680x4320']
    }
    
    res_str = f"{res_X}x{res_Y}"
    for key, value in resolution_mapping.items():
        if res_str in value:
            return key
    return 'Other'

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

        self.logger.info("Feature Engineering...")
        self.dataset['SoftwareIncluded'] = self.dataset['MSOffice'] | self.dataset['Antivirus'] | self.dataset['XboxGamePass']
        self.dataset['AdditionalInput'] = self.dataset['Touchscreen'] | self.dataset['Stylus']
        self.dataset['USB_Ports'] = self.dataset['Number of USB 2.0 Ports'] + self.dataset['Number of USB 3.0 Ports']
        self.dataset['Resolution Type'] = self.dataset.apply(lambda x: categorize_screen_resolution(x['Screen_Resolution_X'], x['Screen_Resolution_Y']), axis=1)
        self.dataset['Price'] = self.dataset['Price'] / 1000
        self.dataset = self.dataset.drop(['Audio Details', 'Form Factor', 'Processor Type', 'Memory Technology', 'Screen_Resolution_X', 'Screen_Resolution_Y', 'HDMI', 'HeadphoneJack', 'USB-C','Number of USB 2.0 Ports', 'Number of USB 3.0 Ports','MSOffice', 'Antivirus', 'XboxGamePass', 'Item Weight', 'Touchscreen', 'Stylus', 'Wifi', 'Ethernet', 'Bluetooth', 'Webcam', 'SDCard', 'Numpad', 'Microphone', 'Thunderbolt', 'Colour', 'Brand', 'is_HDD'], axis=1)

        X = self.dataset.drop('Price', axis=1)
        y = self.dataset['Price']

        self.logger.info(f"Final Input Columns Would be: {X.columns.tolist()}")

        numeric_features = X.select_dtypes(include=[np.number]).columns
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        categorical_features.remove('Product Name')

        
        preprocessor = ColumnTransformer(
            transformers=[
                ('drop_cols', 'drop', ['Product Name']),
                ('num', StandardScaler(), numeric_features),
                ('cat', OrdinalEncoder(), categorical_features),
            ], remainder='passthrough'
        )

        X = preprocessor.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)
        np.save(Path(__file__).parent.parent / 'data/train.npy', np.concatenate((X_train, y_train.values.reshape(-1,1)), axis=1))
        np.save(Path(__file__).parent.parent / 'data/val.npy', np.concatenate((X_val, y_val.values.reshape(-1,1)), axis=1))
        np.save(Path(__file__).parent.parent / 'data/test.npy', np.concatenate((X_test, y_test.values.reshape(-1,1)), axis=1))
        dump(preprocessor, Path(__file__).parent.parent / 'models/preprocessor.joblib')
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 3: Data preprocessing Completed >>>>>>>>>>>>>>>>>')