from flask import Flask, request, jsonify
import pandas as pd
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load model and scaler
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

app = Flask(__name__)

# ✅ Function to send email alert
def send_email_alert(subject, body, to_email):
    from_email = "challaaravind22@gmail.com"  # Replace with your email
    password = "zbdl motr swrw xksi"       # Replace with your Gmail App Password

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        print("✅ Email alert sent successfully.")
    except Exception as e:
        print("❌ Failed to send email alert:", e)

# ✅ Prediction route with email alert if anomaly (-1) is found
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)

        # Normalize column names
        df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

        features = ["cpu_usage", "memory_usage"]
        if not all(col in df.columns for col in features):
            return jsonify({"error": f"Required columns missing: {features}"}), 400

        X_scaled = scaler.transform(df[features])
        predictions = model.predict(X_scaled)

        # ✅ Send email if anomaly is detected
        if -1 in predictions:
            send_email_alert(
                subject="🚨 Anomaly Detected in System Logs",
                body="One or more anomalies (-1) were detected in the uploaded system logs.",
                to_email="challaaravind22@gmail.com"  # Replace with actual email
            )

        return jsonify({"anomalies": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
