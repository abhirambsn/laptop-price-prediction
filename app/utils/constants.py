from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / 'models' / 'best_model.joblib'
PREPROCESSOR_PATH = Path(__file__).parent.parent / 'models' / 'preprocessor.joblib'
CURRENCY_MAPPING = {
    'INR': 'Indian Rupee',
    'EUR': 'Euro', 
    'IDR': 'Indonesian Rupiah', 
    'BGN': 'Bulgarian Lev', 
    'ILS': 'Israeli Shekel', 
    'GBP': 'United Kingdom Pound', 
    'DKK': 'Danish Krone', 
    'CAD': 'Canadian Dollar', 
    'JPY': 'Japanese Yen', 
    'HUF': 'Hungarian Forint', 
    'RON': 'Romanian New Leu', 
    'MYR': 'Malaysian Ringgit', 
    'SEK': 'Swedish Krona', 
    'SGD': 'Singapore Dollar', 
    'HKD': 'Hong Kong Dollar', 
    'AUD': 'Australian Dollar', 
    'CHF': 'Swiss Franc', 
    'KRW': 'Korean (South) Won', 
    'CNY': 'Chinese Yuan Renminbi', 
    'TRY': 'Turkish Lira', 
    'HRK': 'Croatian Kuna', 
    'NZD': 'New Zealand Dollar', 
    'THB': 'Thai Baht', 
    'USD': 'United States Dollar', 
    'NOK': 'Norweigian Krone', 
    'RUB': 'Russian Ruble', 
    'MXN': 'Mexican Peso', 
    'CZK': 'Czech Republic Koruna', 
    'BRL': 'Brazilian Real',
    'PLN': 'Polish Zloty', 
    'PHP': 'Philippines Peso',
    'ZAR': 'South African Rand'
}