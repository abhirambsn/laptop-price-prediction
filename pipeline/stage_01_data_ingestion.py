from pathlib import Path
import pandas as pd
import logging, sys, requests, time, json, threading
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'data_ingestion.log')
s_hnd = logging.StreamHandler(sys.stdout)

def get_description(path):
    if path.startswith("https://"):
        url = path
    else:
        url = "https://amazon.in" + path
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        print(str(resp.status_code)+' - Error loading the page')
        return None
    
def get_product_detail_from_linkPath(path):
    desc_text = get_description(path)
    sp = BeautifulSoup(desc_text, 'html.parser')
    tbl = sp.find('table', {"id": 'productDetails_techSpec_section_1'})
    res = {}
    for row in tbl.findAll("tr"):
        cells = row.findAll("td")
        headers = row.findAll("th")
        data = {i.text.strip(): j.text.strip().strip('\n').strip('\u200e') for i,j in zip(headers, cells)}
        res = {**res, **data}
    return res

class DataIngestion:
    data_path: Path
    data_type: str
    logger: logging.Logger
    sources: List
    n_threads: int

    def __init__(self, data_path: Path, sources: List, n_threads: int = 6):
        self.data_path = data_path
        self.data_type = data_path.suffix
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)
        self.sources = sources
        self.n_threads = n_threads
    
    def fetch_page(self, tid, start, end):
        self.logger.info(f"Thread {tid} started fetching pages from {start} to {end}")
        url = "https://www.amazon.in/s?k=laptops&page={i}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        data = []
        for i in range(start, end):
            self.logger.info(f"Thread {tid} fetching page {i}")
            resp = requests.get(url.format(i=i), headers=headers)
            self.logger.info(f"Fetching Page No.: {i}")
            if resp.status_code == 200:
                data.append({'page': i, 'content': resp.text})
            else:
                print(str(resp.status_code)+' - Error loading the page')
            self.logger.info("Waiting for 2 seconds")
            time.sleep(2)

        self.logger.info("Writing to file data_{start}_{end}.json")
        with open(Path(__file__).parent.parent / 'data' / f'data_{start}_{end}.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Thread {tid} completed fetching pages from {start} to {end}")

    
    def fetch_data_from_source(self, n_threads = 4):
        self.logger.info('Fetching data from sources...')
        threads = []
        filenames = []
        for i in range(n_threads):
            t = threading.Thread(target=self.fetch_page, args=(i+1, i*10, (i+1)*10))
            threads.append(t)
            filenames.append(f'data_{i*10}_{(i+1)*10}.json')
            t.start()
        for t in threads:
            t.join()
        self.logger.info('Data fetched from sources.')
        return filenames
    
    def extract_info(self, files):
        processed_filenames = []
        for idx, file in enumerate(files):
            data = json.load(open(Path(__file__).parent.parent / 'data' / file, 'r'))
            jsonData = []
            for page in data:
                soup = BeautifulSoup(page['content'], 'html.parser')
                ptitle = soup.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'})
                for title in ptitle:
                    self.logger.info("Fetching Data for\t", title.text)
                    pgNo = page['page']
                    price = title.find_next('span', {'class': 'a-price-whole'}).text
                    path = title.find_parent('a')['href']
                    jsonData.append({'Product Name': title.text, 'Page Number': pgNo, 'Price': price, **get_product_detail_from_linkPath(path)})
                    time.sleep(2)
                    with open(f'product_data_{idx}.json', 'w') as f:
                        json.dump(jsonData, f, indent=2)
            processed_filenames.append(f'product_data_{idx}.json')
            
    def combine_files_to_dataset(self, files):
        self.logger.info('Combining files to dataset...')
        dataset = pd.DataFrame()
        for file in files:
            path = Path(__file__).parent.parent / 'data' / file
            df = pd.read_json(path)
            dataset = dataset.append(df)
        dataset.to_csv(self.data_path, index=False)

                
    
    def main(self):
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 1: Data Ingestion Started >>>>>>>>>>>>>>>>>')
        files = self.extract_info(self.fetch_data_from_source(self.n_threads))
        self.combine_files_to_dataset(files)
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 1: Data Ingestion Completed >>>>>>>>>>>>>>>>>')