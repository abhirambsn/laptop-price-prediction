from pathlib import Path
import pandas as pd
import numpy as np
import logging, sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_hnd = logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'data_cleaning.log')
s_hnd = logging.StreamHandler(sys.stdout)

class DataCleaner:
    data_path: Path
    dataset: pd.DataFrame
    data_type: str
    logger: logging.Logger
    cleaned_path: Path

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data_type = data_path.suffix
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(f_hnd)
        self.logger.addHandler(s_hnd)
        self.cleaned_path = Path(str(data_path).replace('raw', 'cleaned'))

        if self.data_type == '.csv':
            self.dataset = pd.read_csv(data_path)
        elif self.data_type == '.json':
            self.dataset = pd.read_json(data_path)
        elif self.data_type == '.xlsx':
            self.dataset = pd.read_excel(data_path)
        else:
            raise Exception('Invalid file type')
        
    def get_null_cols(self):
        cls = list(self.dataset.columns)
        nvs = list(self.dataset.isnull().sum())
        return cls, nvs
    
    def standardize_color(self, color: str):
        if color == np.nan or 'black' in color.lower() or 'carbon' in color.lower():
            return 'Black'
        elif 'silver' in color.lower() or 'moon' in color.lower():
            return 'Silver'
        elif 'grey' in color.lower() or 'gray' in color.lower() or 'graphite' in color.lower():
            return 'Grey'
        elif 'blue' in color.lower():
            return 'Blue'
        return color.split(' ')[-1].capitalize()
    
    def process_form_factor(self, ff: str):
        ff = ff.lower()
        if ff == 'thin and light' or ff == 'thin & light' or ff == 'thin & light laptop':
            return 'thin and light'
        elif ff == 'laptop, chromebook':
            return 'chromebook'
        elif ff == 'gaming laptop' or ff == 'gaming':
            return 'gaming'
        return ff
    
    def process_screen_res(self, res: str):
        if '720p' in res:
            return 1280,720
        elif '1080p' in res:
            return 1920,1080
        elif 'x' in res:
            x,y = res.split('x', maxsplit=1)
            y = y.lstrip(' ').split(' ')[0].strip('_')
            x = x.strip('_').strip(' ')
            if '_' in y:
                y = y.split('_')[0]
            return int(x), int(y)
        elif '*' in res:
            x,y = res.split('*', maxsplit=1)
            y = y.lstrip(' ').split(' ')[0].strip('_')
            x = x.strip('_').strip(' ')
            return int(x), int(y)
        return int(res), int(res)
    
    def process_proc_type(self, tp: str):
        tp1 = tp.lower()
        if 'core i3' in tp1:
            return 'Core i3'
        elif 'core i5' in tp1:
            return 'Core i5'
        elif 'core i7' in tp1:
            return 'Core i7'
        elif 'core i9' in tp1:
            return 'Core i9'
        elif 'celeron' in tp1:
            return 'Celeron'
        elif 'ryzen 3' in tp1:
            return 'Ryzen 3'
        elif 'ryzen 5' in tp1:
            return 'Ryzen 5'
        elif 'ryzen 7' in tp1:
            return 'Ryzen 7'
        elif 'ryzen 9' in tp1:
            return 'Ryzen 9'
        elif 'athlon' in tp1:
            return 'Athlon'
        elif 'others' in tp1 or 'other' in tp1:
            return 'Other'
        return tp
    
    def process_proc_speed(self, sp):
        if isinstance(sp, str):
            return float(sp.split(' ')[0])
        return float(sp)
    
    def process_mem_speed(self, spd):
        if isinstance(spd, str):
            if 'ghz' in spd.lower():
                speed = spd.split(' ')[0]
                if len(speed) != 4:
                    return int(float(speed)*1000)
                return int(speed)
            return int(float(spd.split(' ')[0]))
        return int(spd)
    
    def process_hdd_size(self, size):
        if isinstance(size, str):
            if 'tb' in size.lower():
                return int(size.split(' ')[0])*1000
            return int(size.split(' ')[0])
        return int(size)
    
    def process_graphics_ram(self, gram):
        if isinstance(gram, str):
            if 'gb' in gram.lower():
                size = gram.split(' ')[0]
                if len(size) == 3:
                    return float(size)
                return float(size)*1024
            return float(gram.split(' ')[0])
        return float(gram)*1024
    
    def process_price(self, p):
        if isinstance(p, str):
            return float(p.replace(',', ''))
        return float(p)
    
    def process_item_weight(self, wt):
        splits = wt.split(' ')
        kg = splits[0]
        if len(splits) < 3:
            return float(kg)
        g = splits[2]
        return (float(g)/1000) + float(kg)
    
    def main(self):
        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 2: Data Cleaning Started >>>>>>>>>>>>>>>>>')
        self.logger.info("Removing Un-neceesary columns")
        cls,nvs = self.get_null_cols()
        cols = ['Manufacturer', 'Series', 'Batteries Included', 'Batteries Required', 'Battery cell composition', 'Device type', 'Package Dimensions', 'Mounting Hardware', 'Product Dimensions', 'Voltage', 'Wattage', 'Model', 'Model Name', 'Model Year', 'Power Source', 'Optical Drive Type', 'Are Batteries Included', 'Number of Lithium Ion Cells', 'Lithium Battery Energy Content', 'Item model number', 'Graphics Card Description', 'Graphics RAM Type', 'Graphics Card Interface', 'Connectivity Type', 'Included Components', 'Computer Memory Type', 'Speaker Description', 'Wireless Type', 'Ram Memory Installed Size', 'RAM memory maximum size', 'Ram Memory Technology', 'Processor model number', 'Hardware Interface', 'Hardware Platform', 'Country of Origin', 'Rear Webcam Resolution', 'Hard Disk Rotational Speed', "Memory Storage Capacity", "Chipset Type", "Graphics Coprocessor", "Number of items", 'Flash Memory Installed Size', 'Total USB ports', 'Audio Output Type', 'Item Height', 'Item Width', 'Maximum Memory Supported']
        for i in range(len(cls)):
            if nvs[i] > 1100:
                cols.append(cls[i])
        self.dataset = self.dataset.drop(columns=cols)

        self.logger.info("Filtering out rows with Un-necessary Form Factor")
        self.dataset = self.dataset[self.dataset['Form Factor'] != 'Table Stand']

        self.logger.info("Filling null values in all columns")
        self.dataset['Colour'] = self.dataset['Colour'].fillna('Black')
        self.dataset['Form Factor'] = self.dataset['Form Factor'].fillna('laptop')
        self.dataset.rename(columns={'Standing screen display size': "Screen Resolution"})
        self.dataset['Screen Resolution'] = self.dataset['Screen Resolution'].fillna('720p')
        self.dataset['Processor Brand'] = self.dataset['Processor Brand'].fillna('Other')
        self.dataset['Processor Type'] = self.dataset['Processor Type'].fillna('Other')
        self.dataset['Processor Speed'] = self.dataset['Processor Speed'].astype('object')
        self.dataset['Processor Speed'] = self.dataset['Processor Speed'].fillna('0.0')
        self.dataset['Processor Count'] = self.dataset['Processor Count'].fillna(1)
        self.dataset['RAM Size'] = self.dataset['RAM Size'].fillna('8')
        self.dataset['RAM Size'] = self.dataset['RAM Size'].astype('object')
        self.dataset['Memory Technology'] = self.dataset['Memory Technology'].fillna('DDR4')
        self.dataset['Memory Clock Speed'] = self.dataset['Memory Clock Speed'].fillna('2666')
        self.dataset['Hard Drive Size'] = self.dataset['Hard Drive Size'].fillna('256 GB')
        self.dataset['Hard Disk Description'] = self.dataset['Hard Disk Description'].fillna('HDD')
        self.dataset['Audio Details'] = self.dataset['Audio Details'].fillna('Headphones, Speakers')
        self.dataset['Connector Type'] = self.dataset['Connector Type'].fillna('Wi-Fi, USB, Bluetooth')
        self.dataset['Graphics Chipset Brand'] = self.dataset['Graphics Chipset Brand'].fillna('Integrated')
        self.dataset['Number of USB 2.0 Ports'] = self.dataset['Number of USB 2.0 Ports'].fillna(0)
        self.dataset['Number of USB 3.0 Ports'] = self.dataset['Number of USB 3.0 Ports'].fillna(0)
        self.dataset['Number of HDMI Ports'] = self.dataset['Number of HDMI Ports'].fillna(0)
        self.dataset['Operating System'] = self.dataset['Operating System'].fillna('Windows')
        self.dataset['Graphics Card Ram Size'] = self.dataset['Graphics Card Ram Size'].fillna('0')
        self.dataset['Display Type'] = self.dataset['Display Type'].fillna('LCD')
        self.dataset.rename({'Graphics Card Ram Size': 'GraphicsCardRAM'}, inplace=True, axis=1)
        self.dataset['Average Battery Life (in hours)'] = self.dataset['Average Battery Life (in hours)'].fillna('0')
        self.dataset.rename(columns={'Average Battery Life (in hours)': 'BatteryLife'}, inplace=True)
        self.dataset['Special Features'] = self.dataset['Special Features'].fillna('')
        self.dataset['Software included'] = self.dataset['Software included'].fillna('')
        self.dataset['Keyboard Description'] = self.dataset['Keyboard Description'].fillna('Standard')
        self.dataset['Device interface - primary'] = self.dataset['Device interface - primary'].fillna('Keyboard, Microphone')
        self.dataset['Item Weight'] = self.dataset['Item Weight'].fillna('0 kg 0 g')
        self.dataset = self.dataset.drop('Page Number', axis=1)
        self.logger.info("Null values filled")

        self.logger.info("Cleaning Data")
        self.dataset['Colour'] = self.dataset['Colour'].apply(self.standardize_color)
        self.dataset['Form Factor'] = self.dataset['Form Factor'].apply(self.process_form_factor)
        X,Y = [],[]
        for i in range(len(self.dataset)):
            x,y = self.process_screen_res(self.dataset['Screen Resolution'].iloc[i])
            X.append(x)
            Y.append(y)

        self.dataset['Screen_Resolution_X'] = X
        self.dataset['Screen_Resolution_Y'] = Y
        self.dataset.drop('Screen Resolution', axis=1, inplace=True)
        self.dataset['Processor Type'] = self.dataset['Processor Type'].apply(self.process_proc_type)
        self.dataset['Processor Speed'] = self.dataset['Processor Speed'].apply(self.process_proc_speed)
        self.dataset['Processor Speed'] = self.dataset['Processor Speed'].replace(0.0, round(self.dataset['Processor Speed'].mean(), 2))
        self.dataset['RAM Size'] = self.dataset['RAM Size'].apply(lambda x: int(x.split(' ')[0]))
        self.dataset['Memory Technology'] = self.dataset['Memory Technology'].apply(lambda x: 'LPDDR5' if 'lpddr 5' in x.lower() else x)
        self.dataset['Memory Clock Speed'] = self.dataset['Memory Clock Speed'].apply(self.process_mem_speed)
        self.dataset['is_SSD'] = self.dataset['Hard Disk Description'].apply(lambda x: 1 if 'ssd' in x.lower() or 'sshd' in x.lower() else 0)
        self.dataset['is_HDD'] = self.dataset['Hard Disk Description'].apply(lambda x: 1 if 'hdd' in x.lower() or 'sshd' in x.lower() else 0)
        self.dataset = self.dataset.drop('Hard Disk Description', axis=1)
        self.dataset = self.dataset.drop('Hard Drive Interface', axis=1)
        
        self.dataset.drop('Standing screen display size', axis=1, inplace=True)
        self.dataset.drop('Resolution', axis=1, inplace=True)
        self.dataset.drop('Batteries', axis=1, inplace=True)
        self.dataset['HeadphoneJack'] = self.dataset['Audio Details'].apply(lambda x: 1 if 'headphone' in x.lower() else 0)
        self.dataset['Wifi'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'wi-fi' in x.lower() else 0)
        self.dataset['Bluetooth'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'bluetooth' in x.lower() else 0)
        self.dataset['HDMI'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'hdmi' in x.lower() else 0)
        self.dataset['USB-C'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'usb-c' in x.lower() else 0)
        self.dataset['Ethernet'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'ethernet' in x.lower() else 0)
        self.dataset['Thunderbolt'] = self.dataset['Connector Type'].apply(lambda x: 1 if 'thunderbolt' in x.lower() else 0)
        self.dataset['DedicatedGraphics'] = self.dataset['Graphics Chipset Brand'].apply(lambda x: 1 if 'nvidia' in x.lower() or 'iris' in x.lower() else 0)
        self.dataset['IntegratedGraphics'] = self.dataset['Graphics Chipset Brand'].apply(lambda x: 1 if 'intel' in x.lower() or 'amd' in x.lower() or 'iris' in x.lower() or 'integrated' in x.lower() else 0)
        self.dataset.drop('Graphics Chipset Brand', axis=1, inplace=True)
        self.dataset['Operating System'] = self.dataset['Operating System'].apply(lambda x: 'Windows' if 'windows' in x.lower() else 'MacOS' if 'macos' in x.lower() else 'ChromeOS' if 'chrome' in x.lower() else 'Linux' if 'linux' in x.lower() else 'Other')
        self.dataset['BatteryLife'] = self.dataset['BatteryLife'].apply(lambda x: float(x.split(' ')[0]))
        self.dataset['BatteryLife'] = self.dataset['BatteryLife'].replace(0.0, round(self.dataset['BatteryLife'].mean(), 2))
        self.dataset['Fingerprint'] = self.dataset['Special Features'].apply(lambda x: 1 if 'fingerprint' in x.lower() else 0)
        self.dataset['Webcam'] = self.dataset['Special Features'].apply(lambda x: 1 if 'webcam' in x.lower() or 'camera' in x.lower() else 0)
        self.dataset['SDCard'] = self.dataset['Special Features'].apply(lambda x: 1 if 'memory card' in x.lower() else 0)
        self.dataset = self.dataset.drop('Special Features', axis=1)
        self.dataset['MSOffice'] = self.dataset['Software included'].apply(lambda x: 1 if 'office' in x.lower() else 0)
        self.dataset['Antivirus'] = self.dataset['Software included'].apply(lambda x: 1 if 'antivirus' in x.lower() or 'security' in x.lower() or 'mcafee' in x.lower() else 0)
        self.dataset['XboxGamePass'] = self.dataset['Software included'].apply(lambda x: 1 if 'xbox' in x.lower() else 0)
        self.dataset = self.dataset.drop('Software included', axis=1)
        self.dataset['BacklitKeyboard'] = self.dataset['Keyboard Description'].apply(lambda x: 1 if 'backlit' in x.lower() else 0)
        self.dataset['RGBKeyboard'] = self.dataset['Keyboard Description'].apply(lambda x: 1 if 'rgb' in x.lower() else 0)
        self.dataset = self.dataset.drop('Keyboard Description', axis=1)
        self.dataset['Touchscreen'] = self.dataset['Device interface - primary'].apply(lambda x: 1 if 'touchscreen' in x.lower() else 0)
        self.dataset['Stylus'] = self.dataset['Device interface - primary'].apply(lambda x: 1 if 'stylus' in x.lower() else 0)
        self.dataset['Microphone'] = self.dataset['Device interface - primary'].apply(lambda x: 1 if 'microphone' in x.lower() else 0)
        self.dataset['Numpad'] = self.dataset['Device interface - primary'].apply(lambda x: 1 if 'numeric keypad' in x.lower() else 0)
        self.dataset = self.dataset.drop('Device interface - primary', axis=1)
        self.dataset['Price'] = self.dataset['Price'].apply(self.process_price)
        self.dataset['Item Weight'] = self.dataset['Item Weight'].apply(self.process_item_weight)
        self.logger.info("Data Processed")

        self.logger.info("Saving Cleaned Data")
        self.dataset.to_csv(self.cleaned_path, index=False)
        self.logger.info("Cleaned Data Saved")

        self.logger.info('<<<<<<<<<<<<<<<<< STAGE 2: Data Cleaning Completed >>>>>>>>>>>>>>>>>')