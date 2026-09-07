import os
import joblib
import pandas as pd

from django.conf import settings


MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "wait_time_model.pkl"
)


_model = None


def load_model():
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model


def predict_wait_time_ml(
    patients_ahead,
    queue_length,
    active_doctors,
    avg_consultation_time,
    emergency_load,
    is_walk_in,
    hour,
):
    model = load_model()

    input_data = pd.DataFrame([{
        "patients_ahead": patients_ahead,
        "queue_length": queue_length,
        "active_doctors": active_doctors,
        "avg_consultation_time": avg_consultation_time,
        "emergency_load": emergency_load,
        "is_walk_in": is_walk_in,
        "hour": hour,
    }])

    prediction = model.predict(input_data)[0]

    return max(0, round(float(prediction), 2))