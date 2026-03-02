import pandas as pd
import os
import json
from sklearn.model_selection import train_test_split

# ================= CONFIG =================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "healthcare_dataset.csv")
MERGED_PATH = os.path.join(BASE_DIR, "data", "merged_cleaned.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LABEL_MAP_PATH = os.path.join(BASE_DIR, "models", "label_mapping.json")

TEST_SIZE = 0.2
RANDOM_STATE = 42


def clean_symptoms(symptom_text):
    """
    Clean the Symptoms column and convert to natural sentence.
    """
    if pd.isna(symptom_text):
        return None

    symptom_text = str(symptom_text).replace("_", " ")
    symptom_text = symptom_text.strip()

    # Convert comma-separated symptoms to natural sentence
    sentence = "I have " + symptom_text + "."
    return sentence


def preprocess_dataset():
    print("Loading dataset...")
    df = pd.read_csv(RAW_DATA_PATH)

    print("Original Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # Keep only relevant columns
    df = df[["Symptoms", "Disease"]]

    # Clean text
    df["text"] = df["Symptoms"].apply(clean_symptoms)
    df["label"] = df["Disease"].str.strip().str.title()

    df = df[["text", "label"]]

    # Remove empty rows
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Shuffle
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    print("Cleaned Shape:", df.shape)

    # Save merged cleaned dataset
    df.to_csv(MERGED_PATH, index=False)
    print("Saved cleaned dataset.")

    # Create label mapping
    unique_labels = sorted(df["label"].unique())
    label_mapping = {label: idx for idx, label in enumerate(unique_labels)}

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    with open(LABEL_MAP_PATH, "w") as f:
        json.dump(label_mapping, f, indent=4)

    print("Saved label mapping.")

    # Train-test split
    train_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        stratify=df["label"],
        random_state=RANDOM_STATE
    )

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    train_df.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
    test_df.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False)

    print("Train/Test split saved.")


if __name__ == "__main__":
    preprocess_dataset()