"""
Track_Progress.py
Compare performance of different model versions.
"""

import pandas as pd
import joblib
import glob

df = pd.read_csv('blink_training_data.csv')
X = df[['sum', 'dom']].values
y = df['label'].values

models = glob.glob('blink_model*.pkl')
print("Model Performance on Current Data:")
print("-" * 50)

for model_file in sorted(models):
    model = joblib.load(model_file)
    accuracy = model.score(X, y)
    print(f"{model_file:25} → Accuracy: {accuracy:.3f}")

print("-" * 50)
print(f"Total training samples: {len(df)}")
print(df['label'].value_counts())