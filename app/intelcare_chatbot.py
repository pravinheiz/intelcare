import os
import json
import joblib
import pandas as pd
import numpy as np
import customtkinter as ctk
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import pyaudio
import geocoder
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# =============================
# PATH CONFIGURATION
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "binary_logistic_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "healthcare_dataset.csv")
MEMORY_PATH = os.path.join(BASE_DIR, "models", "chat_memory.json")

# =============================
# LOAD MODEL & DATA
# =============================

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)
symptom_columns = [col.strip().lower() for col in df.columns.tolist()[1:]]

# =============================
# MEMORY SYSTEM
# =============================

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
        data.setdefault("history", [])
        data.setdefault("structured", [])
        return data
    return {"history": [], "structured": []}

def save_memory(mem):
    with open(MEMORY_PATH, "w") as f:
        json.dump(mem, f, indent=4)

memory = load_memory()

# =============================
# SPEECH ENGINE
# =============================

engine = pyttsx3.init()

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# =============================
# GEOLOCATION + OSM
# =============================

def get_user_location():
    try:
        g = geocoder.ip("me")
        if g.latlng:
            return g.latlng
    except:
        return None
    return None

def find_nearby_medical_facilities(lat, lon, radius=5000):
    try:
        query = f"""
        [out:json];
        node
          ["amenity"~"hospital|clinic"]
          (around:{radius},{lat},{lon});
        out;
        """

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            timeout=10
        )

        data = response.json()
        facilities = []

        for element in data.get("elements", [])[:5]:
            name = element["tags"].get("name", "Unnamed Facility")
            facilities.append(name)

        return facilities
    except:
        return []

# =============================
# EMERGENCY DETECTION
# =============================

EMERGENCY_KEYWORDS = [
    "chest pain",
    "fainting",
    "seizure",
    "vomiting blood",
    "paralysis",
    "loss of consciousness"
]

def emergency_check(text):
    return any(word in text.lower() for word in EMERGENCY_KEYWORDS)

# =============================
# PREDICTION ENGINE
# =============================

def create_input_dataframe(user_text):
    input_dict = {symptom: 0 for symptom in symptom_columns}
    matched = []
    for symptom in symptom_columns:
        if symptom in user_text.lower():
            input_dict[symptom] = 1
            matched.append(symptom)
    return pd.DataFrame([input_dict]), matched

def get_top3_predictions(user_text):
    input_df, matched = create_input_dataframe(user_text)
    probabilities = model.predict_proba(input_df)[0]
    top_indices = np.argsort(probabilities)[-3:][::-1]
    results = [(model.classes_[i], probabilities[i] * 100) for i in top_indices]
    return results, matched

# =============================
# SPECIALIST RECOMMENDATION
# =============================

SPECIALIST_MAP = {
    "heart": "Cardiology",
    "stroke": "Neurology",
    "lung": "Pulmonology",
    "pneumonia": "Pulmonology",
    "diabetes": "Endocrinology",
    "arthritis": "Rheumatology"
}

def recommend_specialist(disease):
    for key in SPECIALIST_MAP:
        if key in disease.lower():
            return SPECIALIST_MAP[key]
    return "General Medicine"

# =============================
# TREND ANALYTICS
# =============================

def analyze_trends():
    if not memory["structured"]:
        return "No historical trend data available."
    diseases = [item["Primary Condition"] for item in memory["structured"]]
    most_common = max(set(diseases), key=diseases.count)
    return f"Most frequently recorded condition: {most_common}."

# =============================
# CLINICAL OUTPUT BUILDER
# =============================

def build_clinical_output(top3, matched):
    primary, confidence = top3[0]
    specialist = recommend_specialist(primary)

    output = []
    output.append("Clinical Assessment Summary\n")
    output.append(f"Primary Consideration: {primary}")
    output.append(f"Estimated Likelihood: {confidence:.2f}%\n")

    output.append("Differential Considerations:")
    for disease, conf in top3[1:]:
        output.append(f"- {disease} ({conf:.2f}%)")

    if matched:
        output.append("\nClinical Interpretation:")
        output.append(
            f"Reported symptoms ({', '.join(matched[:5])}) "
            f"correlate with patterns observed in {primary}."
        )

    output.append(f"\nRecommended Specialty: {specialist}")
    output.append(f"\nTrend Analysis: {analyze_trends()}")
    output.append(
        "\nDisclaimer: This system provides informational support only."
    )

    return "\n".join(output), primary, confidence

# =============================
# PDF EXPORT
# =============================

def generate_pdf_report(latest):
    filename = f"clinical_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(BASE_DIR, filename)

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("IntelCare Clinical Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    for key, value in latest.items():
        elements.append(Paragraph(f"{key}: {value}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return path

# =============================
# UI SETUP
# =============================

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x850")
app.title("IntelCare Clinical System")

header = ctk.CTkLabel(app, text="IntelCare Clinical System",
                      font=ctk.CTkFont(size=28, weight="bold"))
header.pack(pady=15)

def toggle_mode():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

mode_switch = ctk.CTkSwitch(app, text="Dark Mode", command=toggle_mode)
mode_switch.pack(pady=(0,10))

chat_box = ctk.CTkTextbox(app, height=500)
chat_box.pack(padx=40, pady=20, fill="both", expand=True)
chat_box.configure(state="disabled")

def add_message(msg):
    chat_box.configure(state="normal")
    chat_box.insert("end", msg + "\n\n")
    chat_box.configure(state="disabled")
    chat_box.see("end")

for item in memory["history"]:
    add_message(item)

input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=40, pady=10)

entry = ctk.CTkEntry(input_frame, height=50)
entry.pack(side="left", fill="x", expand=True, padx=10)

# =============================
# PREMIUM WAVEFORM
# =============================

mic_canvas = ctk.CTkCanvas(input_frame, height=70, highlightthickness=0)
wave_running = False
audio_stream = None
p = None
smoothed_level = 0
silence_counter = 0

def get_wave_colors():
    if ctk.get_appearance_mode() == "Dark":
        return ("#5AC8FA", "#0A84FF")
    else:
        return ("#0A84FF", "#4A90E2")

def gradient_color(start_hex, end_hex, t):
    s = tuple(int(start_hex[i:i+2], 16) for i in (1,3,5))
    e = tuple(int(end_hex[i:i+2], 16) for i in (1,3,5))
    mix = tuple(int(s[i] + (e[i]-s[i]) * t) for i in range(3))
    return f"#{mix[0]:02x}{mix[1]:02x}{mix[2]:02x}"

def start_waveform():
    global wave_running, audio_stream, p
    wave_running = True
    entry.pack_forget()
    mic_canvas.pack(side="left", fill="x", expand=True, padx=10)

    p = pyaudio.PyAudio()
    audio_stream = p.open(format=pyaudio.paInt16, channels=1,
                          rate=44100, input=True, frames_per_buffer=1024)
    animate_waveform()

def stop_waveform():
    global wave_running, audio_stream, p
    wave_running = False

    if audio_stream:
        audio_stream.stop_stream()
        audio_stream.close()
        audio_stream = None

    if p:
        p.terminate()
        p = None

    mic_canvas.delete("all")
    mic_canvas.pack_forget()
    entry.pack(side="left", fill="x", expand=True, padx=10)

def animate_waveform():
    global smoothed_level, silence_counter

    if not wave_running:
        return

    try:
        data = audio_stream.read(1024, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16)
        level = np.abs(samples).mean()
        normalized = min(level/5000, 1.0)
    except:
        normalized = 0

    if normalized < 0.02:
        silence_counter += 1
    else:
        silence_counter = 0

    if silence_counter > 60:
        stop_waveform()
        return

    smoothed_level = smoothed_level*0.8 + normalized*0.2

    mic_canvas.delete("all")

    width = mic_canvas.winfo_width()
    height = 70
    center_y = height//2
    margin = 50
    bars = 45
    spacing = (width - margin*2)/bars
    max_height = 28

    start_color, end_color = get_wave_colors()

    for i in range(bars):
        distance = abs(i - bars//2)
        falloff = max(1 - (distance/(bars/2)), 0)
        bar_height = max(smoothed_level*max_height*falloff, 2)

        x = margin + i*spacing
        y0 = center_y - bar_height
        y1 = center_y + bar_height

        t = i/bars
        color = gradient_color(start_color, end_color, t)

        mic_canvas.create_line(x, y0, x, y1,
                               fill=color, width=4, capstyle="round")

    app.after(30, animate_waveform)

# =============================
# MESSAGE PROCESSING
# =============================

def process_input(user_text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    app.after(0, lambda: add_message(f"Patient Input ({timestamp}): {user_text}"))

    if emergency_check(user_text):
        msg = "🚨 Emergency Alert: Critical symptoms detected."
        app.after(0, lambda: add_message(msg))
        speak("Critical symptoms detected. Locating nearest medical facilities.")

        def emergency_lookup():
            location = get_user_location()
            if location:
                lat, lon = location
                facilities = find_nearby_medical_facilities(lat, lon)
                result = "\nNearest Medical Facilities:\n"
                for f in facilities:
                    result += f"- {f}\n"
            else:
                result = "\nLocation unavailable."

            app.after(0, lambda: add_message(result))

        threading.Thread(target=emergency_lookup, daemon=True).start()
        return

    top3, matched = get_top3_predictions(user_text)
    response, primary, confidence = build_clinical_output(top3, matched)

    app.after(0, lambda: add_message(response))
    speak(response)

    memory["history"].append(f"Patient Input ({timestamp}): {user_text}")
    memory["history"].append(response)
    memory["structured"].append({
        "Timestamp": timestamp,
        "Symptoms": user_text,
        "Primary Condition": primary,
        "Confidence": f"{confidence:.2f}%"
    })
    save_memory(memory)

def send_message():
    text = entry.get().strip()
    if not text:
        return
    entry.delete(0, "end")
    threading.Thread(target=process_input, args=(text,), daemon=True).start()

def speech_input():
    def listen():
        start_waveform()
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        stop_waveform()
        try:
            text = recognizer.recognize_google(audio)
        except:
            text = "Speech not recognized."

        app.after(0, lambda: entry.delete(0,"end"))
        app.after(0, lambda: entry.insert(0,text))
        app.after(0, send_message)

    threading.Thread(target=listen, daemon=True).start()

send_button = ctk.CTkButton(input_frame, text="Submit", command=send_message)
send_button.pack(side="right", padx=10)

mic_button = ctk.CTkButton(input_frame, text="Voice", command=speech_input)
mic_button.pack(side="right", padx=10)

def export_pdf():
    if not memory["structured"]:
        add_message("No structured data available.")
        return
    latest = memory["structured"][-1]
    path = generate_pdf_report(latest)
    add_message(f"Clinical report generated: {path}")

pdf_button = ctk.CTkButton(app, text="Export Clinical Report", command=export_pdf)
pdf_button.pack(pady=10)

app.bind("<Return>", lambda e: send_message())
app.mainloop()