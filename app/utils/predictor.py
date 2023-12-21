import logging
import pandas as pd
from joblib import load
from forex_python.converter import CurrencyRates

class Predictor:
    def __init__(self, model_path, preprocessor_path):
        self.logger = logging.getLogger(__name__)
        try:
            self.model = load(model_path)
            self.preprocessor = load(preprocessor_path)
        except Exception as e:
            self.logger.error("Failed to load model or preprocessor: {}".format(e))
            raise e
    
    def parse_sample(self, sample):
        keys = ['Product Name', 'Processor Brand', 'Processor Speed', 'Processor Count', 
                'RAM Size', 'Memory Clock Speed', 'Hard Drive Size', 'Operating System', 
                'GraphicsCardRAM', 'Number of HDMI Ports', 'BatteryLife', 'Display Type', 
                'is_SSD', 'DedicatedGraphics', 'IntegratedGraphics', 'Fingerprint', 'BacklitKeyboard', 
                'RGBKeyboard', 'SoftwareIncluded', 'AdditionalInput', 'USB_Ports', 'Resolution Type']
    
        return pd.DataFrame([dict(zip(keys, sample))])
    
    def format_prediction(self, prediction, currency):
        c = CurrencyRates()
        price = round(prediction[0],2)*1000
        if currency != "INR":
            price = c.convert('INR', currency, price)
        return f'{round(price, 2):,}'
    
    def predict(self, sample):
        try:
            sample = self.parse_sample(sample)
            sample = self.preprocessor.transform(sample)
            prediction = self.model.predict(sample)
            return prediction
        except Exception as e:
            self.logger.error("Failed to predict: {}".format(e))
            raise e