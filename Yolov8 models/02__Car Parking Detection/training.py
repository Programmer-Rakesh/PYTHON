import os
import cv2
import numpy as np
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle

data = []
labels = []

# Update this with your dataset folder path
DATA_DIR = r"C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 models\02__Car Parking Detection\Dataset"

# Example structure:
# Dataset/
# ├── empty/
# └── not_empty/

CATEGORIES = ['empty', 'not_empty']

for category in CATEGORIES:
    folder = os.path.join(DATA_DIR, category)
    label = 0 if category == 'empty' else 1

    for file in os.listdir(folder):
        try:
            img_path = os.path.join(folder, file)
            img = cv2.imread(img_path)
            img = resize(img, (15, 15, 3))  # same as used in util.py
            data.append(img.flatten())
            labels.append(label)
        except Exception as e:
            print(f"Error reading {img_path}: {e}")

X = np.array(data)
y = np.array(labels)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM model
model = SVC()
model.fit(X_train, y_train)

# Save model
with open("model.p", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.p")

