"""
Train_the_ML_Model.py
Run after collecting data to create a model that predicts left/right/no wink from SUM and DOM.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load data
df = pd.read_csv('blink_training_data.csv')
print(f"Loaded {len(df)} samples")

# Show class distribution
print("\nClass distribution:")
print(df['label'].value_counts())

# Prepare features and labels
X = df[['sum', 'dom']].values
y = df['label'].values  # 'l', 'r', 'n'

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest accuracy: {accuracy:.2f} ({accuracy*100:.1f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
print("\nFeature importance:")
for name, imp in zip(['sum', 'dom'], model.feature_importances_):
    print(f"  {name}: {imp:.3f}")

# Save model
joblib.dump(model, 'blink_model.pkl')
print("\n✓ Model saved as 'blink_model.pkl'")