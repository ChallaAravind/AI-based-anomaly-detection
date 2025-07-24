import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle

# Generate training data
data = {
    "cpu_usage": np.random.normal(loc=50, scale=10, size=1000),
    "memory_usage": np.random.normal(loc=30, scale=5, size=1000)
}
df = pd.DataFrame(data)

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["cpu_usage", "memory_usage"]])

# Train IsolationForest
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_scaled)

# Save model and scaler
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model and scaler trained and saved.")
