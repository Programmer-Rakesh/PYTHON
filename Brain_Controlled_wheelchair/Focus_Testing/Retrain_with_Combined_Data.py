"""
retrain_model.py - Run this anytime you want to improve the model
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

# Load ALL data (old + new)
print("Loading training data...")
df = pd.read_csv('training_data.csv')
print(f"Total samples: {len(df)}")

# Show class distribution
print("\nSamples per class:")
print(df['label'].value_counts())

# Prepare data
X = df[['betaL', 'betaR', 'alphaL', 'alphaR']].values
label_map = {'r': 0, 'v': 1, 'm': 2}
y = df['label'].map(label_map).values

# Cross-validation to check stability
print("\nPerforming 5-fold cross-validation...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")

# Train final model on all data
model.fit(X, y)

# Save improved model
joblib.dump(model, 'focus_model_v2.pkl')
print("\n✓ Improved model saved as 'focus_model_v2.pkl'")

# Optional: Keep version history
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
joblib.dump(model, f'focus_model_{timestamp}.pkl')
print(f"✓ Backup saved as 'focus_model_{timestamp}.pkl'")

# Compare with previous model if exists
try:
    old_model = joblib.load('focus_model.pkl')
    old_score = old_model.score(X, y)
    new_score = model.score(X, y)
    print(f"\nPrevious model accuracy: {old_score:.3f}")
    print(f"New model accuracy:      {new_score:.3f}")
    print(f"Improvement:             {new_score - old_score:+.3f}")
except:
    print("\nNo previous model to compare")