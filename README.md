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

# 🧠 System Architecture

## Layered Architecture

Presentation Layer\
- CustomTkinter GUI\
- Voice Waveform Visualization

Interaction Layer\
- Speech Recognition\
- Text Input

Clinical Logic Layer\
- Emergency Detection\
- Specialist Mapping\
- Trend Analytics

Machine Learning Layer\
- Logistic Regression Classifier

Data Layer\
- Model File (.pkl)\
- Dataset\
- Memory JSON

------------------------------------------------------------------------

# 📊 UML Component Diagram

User → GUI → Symptom Parser → ML Model → Clinical Layer → Output →
Memory Storage → PDF Export

------------------------------------------------------------------------

# 🔄 Runtime Flow

1.  User enters symptoms (text or voice)
2.  Speech converted to text (if voice used)
3.  Symptoms mapped to binary feature vector
4.  Model predicts probability distribution
5.  Top 3 predictions extracted
6.  Emergency check executed
7.  Specialist recommended
8.  Output displayed and spoken
9.  Data stored in persistent memory
10. Optional PDF export generated

------------------------------------------------------------------------

# 🌍 Deployment Architecture

## Local Deployment

-   Python Runtime
-   CustomTkinter GUI
-   Scikit-learn Model
-   SpeechRecognition + PyAudio
-   OpenStreetMap API
-   ReportLab PDF Generator

## Future Cloud Deployment

Frontend (Web UI)\
↓\
FastAPI Backend\
↓\
Dockerized ML Inference\
↓\
Secure Encrypted Database

------------------------------------------------------------------------

# 📚 Research-Oriented Framing

## Problem Statement

Early-stage symptom interpretation lacks accessible digital
decision-support systems that combine probabilistic reasoning with
ethical medical framing.

## Objective

To design a modular AI-driven clinical support system that:

-   Performs probabilistic symptom-disease mapping
-   Provides emergency escalation logic
-   Maintains conservative output framing
-   Integrates voice-based interaction
-   Preserves structured historical logs

## Methodology

-   Supervised multi-class classification
-   Logistic Regression baseline model
-   Binary feature encoding
-   Top-3 probabilistic output ranking
-   Keyword-based emergency override
-   OpenStreetMap facility lookup

## Evaluation

-   Validation Accuracy: \~85%
-   Structured output verification
-   Emergency detection override testing
-   Multi-session memory persistence validation

## Limitations

-   Dataset-driven bias
-   No laboratory integration
-   No imaging integration
-   No real-time physiological monitoring
-   IP-based geolocation limitations

------------------------------------------------------------------------

# ⚖️ Ethical AI Statement

IntelCare adheres to the following principles:

-   Non-diagnostic framing
-   Human-in-the-loop validation
-   Emergency-first override logic
-   Conservative confidence interpretation
-   Transparency of limitations

The system is intentionally constrained to prevent overconfidence and
automated clinical authority.

------------------------------------------------------------------------

## 📂 Dataset

The dataset is hosted externally due to GitHub's 100MB file limit.

Download here:
https://drive.google.com/uc?export=download&id=1oWSRdZuoT9YIBb4-UG2ZJ-6ijyIbErgK

After downloading, place the file inside:

data/raw/healthcare_dataset.csv
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
