from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model
try:
    model = pickle.load(open("model.pkl", "rb"))
    expected_features = ['cpu_usage', 'memory_usage']
except Exception as e:
    print("Error loading model:", e)
    model = None
    expected_features = []

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Convert to DataFrame
        df = pd.DataFrame(data)

        print("Converted DataFrame:")
        print(df.head())

        # Replace NaN with None to ensure JSON compliance if you return it
        df.replace({np.nan: None}, inplace=True)

        # Check for expected columns
        if not all(feature in df.columns for feature in expected_features):
            return jsonify({
                "error": f"CSV file must contain these columns: {expected_features}. Received: {list(df.columns)}"
            })

        # If model is None, return error
        if model is None:
            return jsonify({"error": "Model not loaded"})

        # Predict
        predictions = model.predict(df)

        return jsonify({"anomalies": predictions.tolist()})
    except Exception as e:
        print("Error in prediction:", e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
