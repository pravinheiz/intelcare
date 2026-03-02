import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# ================= PATH CONFIG =================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "healthcare_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "binary_logistic_model.pkl")

# ================= LOAD DATA =================

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)

# ================= FEATURES & LABEL =================

if "diseases" not in df.columns:
    raise ValueError("Column 'diseases' not found in dataset")

# Remove rare diseases
disease_counts = df["diseases"].value_counts()

# Keep diseases with at least 50 samples
valid_diseases = disease_counts[disease_counts >= 50].index

df = df[df["diseases"].isin(valid_diseases)]

print("Remaining classes:", df["diseases"].nunique())
print("New dataset shape:", df.shape)

X = df.drop(columns=["diseases"])
y = df["diseases"]

print("Number of features:", X.shape[1])
print("Number of classes:", y.nunique())

# ================= TRAIN TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ================= MODEL =================

model = LogisticRegression(
    max_iter=1000,
    n_jobs=-1
)

print("Training model...")
model.fit(X_train, y_train)

# ================= EVALUATION =================

preds = model.predict(X_test)

accuracy = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds, average="weighted")

print("\n===== Evaluation Results =====")
print("Accuracy:", accuracy)
print("F1 Score:", f1)

print("\nClassification Report:")
print(classification_report(y_test, preds))

# ================= SAVE MODEL =================

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("\nModel saved to:", MODEL_PATH)