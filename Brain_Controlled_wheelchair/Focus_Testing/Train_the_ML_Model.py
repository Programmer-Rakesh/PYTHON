"""
CODE 2: train_model.py
Run this after collecting data to create the ML model
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

# Load the training data
print("Loading training data...")
df = pd.read_csv('training_data.csv')
print(f"Loaded {len(df)} samples")

# Display class distribution
print("\nClass distribution:")
print(df['label'].value_counts())

# Prepare features (X) and labels (y)
feature_columns = ['betaL', 'betaR', 'alphaL', 'alphaR']
X = df[feature_columns].values

# Convert labels to numbers: r=0 (relaxed), v=1 (visual), m=2 (motor)
label_map = {'r': 0, 'v': 1, 'm': 2}
y = df['label'].map(label_map).values

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Create and train the model
print("\nTraining Random Forest classifier...")
model = RandomForestClassifier(
    n_estimators=100,      # 100 trees
    max_depth=10,           # Limit tree depth to prevent overfitting
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✓ Model accuracy: {accuracy:.2f} ({accuracy*100:.1f}%)")

# Detailed performance report
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred, 
                           target_names=['Relaxed', 'Visual Focus', 'Motor Focus']))

# Show feature importance
importance = model.feature_importances_
print("\nFeature Importance:")
for name, imp in zip(feature_columns, importance):
    print(f"  {name}: {imp:.3f}")

# Save the trained model
joblib.dump(model, 'focus_model.pkl')
print("\n✓ Model saved as 'focus_model.pkl'")

# Optional: Create a simple threshold-based classifier for comparison
print("\n" + "="*50)
print("If accuracy is below 70%, consider collecting more data")
print("You can now run realtime_control.py")