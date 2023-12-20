from pathlib import Path
import pandas as pd
import logging, sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'data_ingestion.log')
s_hnd = logging.StreamHandler(sys.stdout)

class DataIngestion:
    data_path: Path
    dataset: pd.DataFrame
    data_type: str
    logger: logging.Logger

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
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 1: Data ingestion Started >>>>>>>>>>>>>>>>>')
        self.logger.info(f'Data type: {self.data_type}')
        self.logger.info(f'Data shape: {self.dataset.shape}')
        self.logger.info(f'Data columns: {self.dataset.columns}')
        self.logger.info(f'Data head: {self.dataset.head()}')
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 1: Data ingestion Completed >>>>>>>>>>>>>>>>>')