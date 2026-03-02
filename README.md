# IntelCare Clinical System -- Complete Documentation

**Author:** Heisnam Pravin Singh\
**Generated on:** 2026-03-02 07:14:14

------------------------------------------------------------------------

# 📄 Academic Abstract

## Abstract

IntelCare is a Clinical Decision Support (CDS) system designed to assist
in preliminary symptom-based medical risk assessment using supervised
machine learning techniques. The system employs a multi-class Logistic
Regression classifier trained on structured symptom-disease datasets to
generate probabilistic disease predictions.

The application integrates real-time speech recognition, waveform-based
voice visualization, geolocation-assisted emergency facility lookup via
OpenStreetMap, and structured clinical output generation within a
desktop GUI environment.

Unlike autonomous diagnostic systems, IntelCare is intentionally
engineered as a conservative decision-support tool. It emphasizes
probabilistic interpretation, emergency override mechanisms, and ethical
output framing to mitigate risks associated with overconfidence in
AI-assisted medical reasoning.

The system demonstrates approximately 85% classification accuracy on
validation data; however, outputs are explicitly framed as "Primary
Considerations" rather than diagnoses, reinforcing human-in-the-loop
clinical validation.

------------------------------------------------------------------------

# 📦 Installation Guide

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Internet connection** (for speech recognition and geolocation services)
- **Microphone** (for voice input feature)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/intelcare.git
cd intelcare
```

## Step 2: Install Dependencies

The project includes a `requirements.txt` file with all necessary dependencies. Install using pip:

```bash
pip install -r requirements.txt
```

### Contents of requirements.txt:
```
customtkinter>=5.2.0
pyttsx3>=2.90
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
pandas>=2.0.0
numpy>=1.24.0
joblib>=1.3.0
geocoder>=1.38.1
requests>=2.31.0
reportlab>=4.0.0
```

### Platform-Specific Notes for PyAudio

#### For Windows:
- PyAudio usually installs without issues via pip
- If you encounter errors, download the appropriate wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

#### For macOS:
```bash
brew install portaudio
pip install pyaudio
```

#### For Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

## Step 3: Download the Dataset

The dataset is hosted externally due to GitHub's 100MB file limit.

**Download link:** https://drive.google.com/uc?export=download&id=1oWSRdZuoT9YIBb4-UG2ZJ-6ijyIbErgK

After downloading, create the required directory structure and place the file:

```bash
mkdir -p data/raw
# Move the downloaded file to:
# data/raw/healthcare_dataset.csv
```

## Step 4: Verify Model File

The pre-trained model is already included in the repository. Verify its location:

```bash
# The model should be at:
# models/binary_logistic_model.pkl

# To verify:
ls -la models/binary_logistic_model.pkl
```

If the model file is missing, ensure you've cloned the repository completely:
```bash
git lfs pull  # If using Git LFS
# or simply reclone:
git clone https://github.com/yourusername/intelcare.git
```

## Step 5: Run the Application

The main application is located in the `app` directory:

```bash
python app/intelcare_chatbot.py
```

## Quick Start (All Steps in One)

```bash
# Clone and setup
git clone https://github.com/yourusername/intelcare.git
cd intelcare

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create data directory and download dataset
mkdir -p data/raw
# Manually download dataset from Google Drive link above
# Place it in data/raw/healthcare_dataset.csv

# Verify model exists
ls models/binary_logistic_model.pkl

# Run the application
python app/intelcare_chatbot.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PyAudio installation fails | Install system audio drivers first (see platform-specific notes) |
| Speech recognition not working | Check microphone permissions |
| Model file not found | Run `ls models/` to verify; reclone if missing |
| Dataset not found | Download from Google Drive link |
| "No module named 'customtkinter'" | Run `pip install -r requirements.txt` again |
| File not found error | Ensure you're running from the project root directory |

------------------------------------------------------------------------

# 🧠 System Architecture

## Layered Architecture

**Presentation Layer**
- CustomTkinter GUI
- Voice Waveform Visualization

**Interaction Layer**
- Speech Recognition
- Text Input

**Clinical Logic Layer**
- Emergency Detection
- Specialist Mapping
- Trend Analytics

**Machine Learning Layer**
- Logistic Regression Classifier

**Data Layer**
- Model File (.pkl)
- Dataset
- Memory JSON

------------------------------------------------------------------------

# 📊 UML Component Diagram

```
User → GUI → Symptom Parser → ML Model → Clinical Layer → Output → Memory Storage → PDF Export
```

------------------------------------------------------------------------

# 🔄 Runtime Flow

1. User enters symptoms (text or voice)
2. Speech converted to text (if voice used)
3. Symptoms mapped to binary feature vector
4. Model predicts probability distribution
5. Top 3 predictions extracted
6. Emergency check executed
7. Specialist recommended
8. Output displayed and spoken
9. Data stored in persistent memory
10. Optional PDF export generated

------------------------------------------------------------------------

# 📁 Project Structure

```
intelcare/
│
├── app/
│   └── intelcare_chatbot.py      # Main application entry point
│
├── models/
│   └── binary_logistic_model.pkl  # Pre-trained ML model
│
├── data/
│   └── raw/
│       └── healthcare_dataset.csv  # Training dataset (download separately)
│
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

------------------------------------------------------------------------

# 🌍 Deployment Architecture

## Local Deployment

- Python Runtime
- CustomTkinter GUI
- Scikit-learn Model
- SpeechRecognition + PyAudio
- OpenStreetMap API
- ReportLab PDF Generator

## Future Cloud Deployment

```
Frontend (Web UI)
↓
FastAPI Backend
↓
Dockerized ML Inference
↓
Secure Encrypted Database
```

------------------------------------------------------------------------

# 📚 Research-Oriented Framing

## Problem Statement

Early-stage symptom interpretation lacks accessible digital
decision-support systems that combine probabilistic reasoning with
ethical medical framing.

## Objective

To design a modular AI-driven clinical support system that:

- Performs probabilistic symptom-disease mapping
- Provides emergency escalation logic
- Maintains conservative output framing
- Integrates voice-based interaction
- Preserves structured historical logs

## Methodology

- Supervised multi-class classification
- Logistic Regression baseline model
- Binary feature encoding
- Top-3 probabilistic output ranking
- Keyword-based emergency override
- OpenStreetMap facility lookup

## Evaluation

- Validation Accuracy: ~85%
- Structured output verification
- Emergency detection override testing
- Multi-session memory persistence validation

## Limitations

- Dataset-driven bias
- No laboratory integration
- No imaging integration
- No real-time physiological monitoring
- IP-based geolocation limitations

------------------------------------------------------------------------

# ⚖️ Ethical AI Statement

IntelCare adheres to the following principles:

- Non-diagnostic framing
- Human-in-the-loop validation
- Emergency-first override logic
- Conservative confidence interpretation
- Transparency of limitations

The system is intentionally constrained to prevent overconfidence and
automated clinical authority.

------------------------------------------------------------------------

# 📂 Dataset Information

The dataset is hosted externally due to GitHub's 100MB file limit.

**Download:** https://drive.google.com/uc?export=download&id=1oWSRdZuoT9YIBb4-UG2ZJ-6ijyIbErgK

**Placement:**
```
data/raw/healthcare_dataset.csv
```

## Dataset Schema

| Column | Description |
|--------|-------------|
| symptom_1 | Binary indicator |
| symptom_2 | Binary indicator |
| ... | ... |
| disease | Target label |

------------------------------------------------------------------------

# 🤖 Model Information

The pre-trained Logistic Regression model is included in the repository:

**Location:** `models/binary_logistic_model.pkl`

**Model Details:**
- Algorithm: Multi-class Logistic Regression
- Features: Binary symptom indicators
- Output: Probability distribution across disease classes
- Accuracy: ~85% on validation set

------------------------------------------------------------------------

# 📜 MIT License

MIT License

Copyright (c) 2026 Heisnam Pravin Singh

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY.
