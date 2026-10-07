import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


DATA_PATH = "data/electrical_data.csv"
MODEL_PATH = "models/fault_model.pkl"


def train_model():
    data = pd.read_csv(DATA_PATH)

    features = [
        "voltage",
        "current",
        "frequency",
        "power_factor",
        "temperature",
    ]

    X = data[features]

    encoder = LabelEncoder()
    y = encoder.fit_transform(data["fault"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(
        {
            "model": model,
            "encoder": encoder,
            "features": features,
        },
        MODEL_PATH,
    )

    return accuracy


def predict_fault(voltage, current, frequency, power_factor, temperature):
    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    encoder = saved_data["encoder"]
    features = saved_data["features"]

    input_data = pd.DataFrame(
        [[
            voltage,
            current,
            frequency,
            power_factor,
            temperature,
        ]],
        columns=features,
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities)

    fault = encoder.inverse_transform([prediction])[0]

    return fault, confidence