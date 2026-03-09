"""
track_progress.py - See how your model improves over time
"""

import pandas as pd
import joblib
import glob

# Load all data
df = pd.read_csv('training_data.csv')
X = df[['betaL', 'betaR', 'alphaL', 'alphaR']].values
label_map = {'r': 0, 'v': 1, 'm': 2}
y = df['label'].map(label_map).values

# Find all saved models
models = glob.glob('focus_model*.pkl')
print("Model Performance Over Time:")
print("-" * 50)

for model_file in sorted(models):
    model = joblib.load(model_file)
    accuracy = model.score(X, y)
    print(f"{model_file:25} → Accuracy: {accuracy:.3f}")

print("-" * 50)
print(f"Total training samples: {len(df)}")
print(f"Classes: {df['label'].value_counts().to_dict()}")