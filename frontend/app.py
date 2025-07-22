import streamlit as st
import requests
import pandas as pd

st.title("System Log Anomaly Detection")

uploaded_file = st.file_uploader("Upload a CSV log file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:", df.head())
    if st.button("Detect Anomalies"):
        try:
            response = requests.post("http://localhost:5000/predict", json=df.to_dict(orient='records'))
            if response.status_code == 200:
                result = response.json()
                df['Anomaly'] = result['anomalies']
                st.write("Detection Results:", df)
            else:
                st.error("Backend Error: " + response.text)
        except Exception as e:
            st.error("Error contacting backend: " + str(e))
