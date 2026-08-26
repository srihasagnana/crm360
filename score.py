import json
import joblib
import pandas as pd
from azureml.core.model import Model

model = None


def init():
    global model

    model_path = Model.get_model_path("crm360-churn-rf")
    model = joblib.load(model_path)

    print("Model loaded successfully")


def run(raw_data):
    try:
        data = json.loads(raw_data)

        if isinstance(data, dict):
            data = [data]

        df = pd.DataFrame(data)

        prediction = model.predict(df)

        probability = model.predict_proba(df)

        return {
            "prediction": prediction.tolist(),
            "probability": probability.tolist()
        }

    except Exception as e:
        return {
            "error": str(e)
        }