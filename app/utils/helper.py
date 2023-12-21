from . import Predictor, MODEL_PATH, PREPROCESSOR_PATH

def predict_price(data, currency="INR"):
    print(f"Predicting Price for {data['Product Name']} in Currency {currency}")
    predictor = Predictor(MODEL_PATH, PREPROCESSOR_PATH)
    prediction = predictor.predict(data.values())
    return predictor.format_prediction(prediction, currency)

def get_currency(c_str):
    return c_str.split(" - ")[0].strip()