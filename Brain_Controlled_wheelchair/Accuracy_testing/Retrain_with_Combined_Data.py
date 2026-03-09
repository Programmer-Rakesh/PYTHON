"""
Retrain_with_Combined_Data.py
Run this after adding new data to retrain and improve the model.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib

df = pd.read_csv('blink_training_data.csv')
print(f"Total samples: {len(df)}")
print("Class distribution:")
print(df['label'].value_counts())

X = df[['sum', 'dom']].values
y = df['label'].values

# Cross-validation to check stability
model = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=5)
print(f"\nCross-validation accuracy: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")

# Train on all data
model.fit(X, y)

# Save new model
joblib.dump(model, 'blink_model_v2.pkl')
print("✓ New model saved as 'blink_model_v2.pkl'")

# Optionally keep a timestamped backup
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
joblib.dump(model, f'blink_model_{timestamp}.pkl')
print(f"✓ Backup saved as 'blink_model_{timestamp}.pkl'")