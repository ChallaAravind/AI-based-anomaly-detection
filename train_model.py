import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

# Sample log-like data
data = {
    "timestamp": pd.date_range(start='2023-01-01', periods=100, freq='H'),
    "cpu_usage": np.random.normal(loc=50, scale=10, size=100),
    "memory_usage": np.random.normal(loc=30, scale=5, size=100)
}

df = pd.DataFrame(data)

# Train model
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(df[["cpu_usage", "memory_usage"]])

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("✅ Model trained and saved as model.pkl")
