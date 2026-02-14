from flask import Flask, request, jsonify
import joblib
import pandas as pd

model = joblib.load("churn_model.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return "Churn Prediction API Running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        df = pd.DataFrame([data])

        # ---- prevent infinity ----
        df["tenure"] = df["tenure"].clip(lower=1)

        # ---- engineered features ----
        df["charge_per_tenure"] = df["monthly_charge"] / (df["tenure"] + 1)
        df["income_per_family"] = df["income_numeric"] / (df["tenure"] + 1)

        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]

        return jsonify({
            "prediction": int(pred),
            "probability": float(prob)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
