# src/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import os
import re

# ── Load model and symptom list ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path   = os.path.join(BASE_DIR, "model", "model.pkl")
symptom_path = os.path.join(BASE_DIR, "model", "symptoms.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(symptom_path, "rb") as f:
    symptoms = pickle.load(f)

# ── Flask App ────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# ── Disease → Specialty + Health Suggestion Map ──────────────────────
DISEASE_INFO = {
    "(vertigo) Paroymsal  Positional Vertigo": {
        "specialty": "Neurologist",
        "specialty_icon": "🧠",
        "suggestions": [
            "Perform Epley maneuver exercises as advised by your doctor.",
            "Avoid sudden head movements; rise slowly from lying/sitting positions.",
            "Stay hydrated and limit caffeine and alcohol.",
            "Rest in a quiet, dimly lit room during episodes."
        ]
    },
    "AIDS": {
        "specialty": "Infectious Disease Specialist",
        "specialty_icon": "🦠",
        "suggestions": [
            "Consult an infectious disease specialist urgently for antiretroviral therapy (ART).",
            "Get regular CD4 count and viral load monitoring.",
            "Practice safe sex and inform close contacts.",
            "Maintain a healthy diet to support immune function."
        ]
    },
    "Acne": {
        "specialty": "Dermatologist",
        "specialty_icon": "🧴",
        "suggestions": [
            "Wash your face twice daily with a gentle, non-comedogenic cleanser.",
            "Avoid touching or picking at affected areas.",
            "Use oil-free, non-comedogenic moisturizers and sunscreen.",
            "Over-the-counter benzoyl peroxide or salicylic acid can help mild cases."
        ]
    },
    "Alcoholic hepatitis": {
        "specialty": "Gastroenterologist / Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Stop alcohol consumption completely — this is critical.",
            "Seek immediate medical attention; hospitalization may be required.",
            "Follow a high-protein, high-calorie nutritional plan.",
            "Join an alcohol cessation support program."
        ]
    },
    "Allergy": {
        "specialty": "Allergist / Immunologist",
        "specialty_icon": "🌿",
        "suggestions": [
            "Identify and avoid known allergen triggers.",
            "Keep antihistamines handy for allergic reactions.",
            "Consider allergy testing to identify specific triggers.",
            "Keep windows closed during high-pollen seasons."
        ]
    },
    "Arthritis": {
        "specialty": "Rheumatologist",
        "specialty_icon": "🦴",
        "suggestions": [
            "Engage in low-impact exercises like swimming or cycling.",
            "Apply warm or cold compresses to affected joints for relief.",
            "Maintain a healthy weight to reduce joint stress.",
            "Use prescribed anti-inflammatory medications as directed."
        ]
    },
    "Bronchial Asthma": {
        "specialty": "Pulmonologist",
        "specialty_icon": "🫁",
        "suggestions": [
            "Always carry your prescribed rescue inhaler.",
            "Identify and avoid asthma triggers (dust, smoke, pets).",
            "Monitor breathing with a peak flow meter daily.",
            "Follow your asthma action plan strictly."
        ]
    },
    "Cervical spondylosis": {
        "specialty": "Orthopedist / Neurologist",
        "specialty_icon": "🦴",
        "suggestions": [
            "Do physiotherapy-recommended neck exercises regularly.",
            "Maintain good posture, especially when using screens.",
            "Use a cervical pillow for neck support during sleep.",
            "Avoid prolonged static neck positions."
        ]
    },
    "Chicken pox": {
        "specialty": "General Physician / Infectious Disease Specialist",
        "specialty_icon": "🩺",
        "suggestions": [
            "Stay isolated to prevent spreading the virus.",
            "Apply calamine lotion to relieve itching.",
            "Trim fingernails short to avoid scratching blisters.",
            "Stay hydrated and rest well; fever reducers may help."
        ]
    },
    "Chronic cholestasis": {
        "specialty": "Gastroenterologist / Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Avoid alcohol and hepatotoxic medications.",
            "Follow a low-fat diet to ease bile flow.",
            "Get regular liver function tests.",
            "Discuss bile acid medications with your specialist."
        ]
    },
    "Common Cold": {
        "specialty": "General Physician",
        "specialty_icon": "🩺",
        "suggestions": [
            "Rest well and stay hydrated with water and warm fluids.",
            "Use saline nasal spray to relieve congestion.",
            "Honey and ginger tea can soothe throat irritation.",
            "Avoid spreading — wash hands frequently and cover coughs."
        ]
    },
    "Dengue": {
        "specialty": "Infectious Disease Specialist",
        "specialty_icon": "🦠",
        "suggestions": [
            "Seek immediate medical care — severe dengue can be life-threatening.",
            "Drink plenty of fluids to prevent dehydration.",
            "Rest and take paracetamol for fever (avoid ibuprofen/aspirin).",
            "Use mosquito repellent and eliminate standing water."
        ]
    },
    "Diabetes ": {
        "specialty": "Endocrinologist",
        "specialty_icon": "🩸",
        "suggestions": [
            "Monitor your blood glucose levels regularly.",
            "Follow a low-glycaemic diet — avoid sugary and processed foods.",
            "Exercise for at least 30 minutes most days of the week.",
            "Take prescribed medications (insulin/oral hypoglycaemics) consistently."
        ]
    },
    "Dimorphic hemmorhoids(piles)": {
        "specialty": "Gastroenterologist / Proctologist",
        "specialty_icon": "🏥",
        "suggestions": [
            "Increase dietary fiber intake (fruits, vegetables, whole grains).",
            "Drink at least 8 glasses of water daily.",
            "Avoid straining during bowel movements.",
            "Sitz baths (warm water soaks) can relieve discomfort."
        ]
    },
    "Drug Reaction": {
        "specialty": "Allergist / Emergency Physician",
        "specialty_icon": "⚕️",
        "suggestions": [
            "Stop the suspected medication immediately and seek medical help.",
            "Carry a list of all your allergies to every medical appointment.",
            "Do not restart the medication without specialist approval.",
            "Wear a medical alert bracelet if you have severe drug allergies."
        ]
    },
    "Fungal infection": {
        "specialty": "Dermatologist",
        "specialty_icon": "🧴",
        "suggestions": [
            "Keep affected areas clean and completely dry.",
            "Apply prescribed antifungal creams as directed.",
            "Wear breathable, cotton clothing and change socks daily.",
            "Avoid sharing personal items like towels or shoes."
        ]
    },
    "GERD": {
        "specialty": "Gastroenterologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Avoid spicy, acidic, and fatty foods.",
            "Eat smaller, more frequent meals; don't lie down after eating.",
            "Elevate the head of your bed by 6–8 inches.",
            "Avoid caffeine, alcohol, and smoking."
        ]
    },
    "Gastroenteritis": {
        "specialty": "Gastroenterologist / General Physician",
        "specialty_icon": "🩺",
        "suggestions": [
            "Stay hydrated with oral rehydration salts (ORS).",
            "Eat bland foods (BRAT diet: bananas, rice, applesauce, toast).",
            "Rest and avoid dairy and fatty foods temporarily.",
            "Seek care if vomiting lasts more than 2 days or blood appears."
        ]
    },
    "Heart attack": {
        "specialty": "Cardiologist — SEEK EMERGENCY CARE IMMEDIATELY",
        "specialty_icon": "🚨",
        "suggestions": [
            "Call emergency services (911 / 1990) IMMEDIATELY.",
            "Chew an aspirin (325 mg) if not allergic, while waiting for help.",
            "Stay calm and avoid physical exertion.",
            "Do not drive yourself — wait for emergency services."
        ]
    },
    "Hepatitis B": {
        "specialty": "Gastroenterologist / Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Consult a hepatologist for antiviral treatment options.",
            "Avoid alcohol completely to protect your liver.",
            "Ensure family members and close contacts are vaccinated.",
            "Get regular liver ultrasounds and blood tests."
        ]
    },
    "Hepatitis C": {
        "specialty": "Gastroenterologist / Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Direct-acting antiviral (DAA) therapy can cure hepatitis C — consult your specialist.",
            "Avoid alcohol to reduce liver damage.",
            "Do not share needles, razors, or personal care items.",
            "Get vaccinated against hepatitis A and B."
        ]
    },
    "Hepatitis D": {
        "specialty": "Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Hepatitis D only occurs with hepatitis B — urgent specialist care needed.",
            "Interferon-alpha therapy may be recommended.",
            "Avoid alcohol completely.",
            "Regular liver function monitoring is essential."
        ]
    },
    "Hepatitis E": {
        "specialty": "Gastroenterologist / Infectious Disease Specialist",
        "specialty_icon": "🦠",
        "suggestions": [
            "Ensure safe drinking water and proper sanitation.",
            "Bed rest and hydration are the primary treatments.",
            "Avoid alcohol during recovery.",
            "Pregnant patients should seek urgent care."
        ]
    },
    "Hypertension ": {
        "specialty": "Cardiologist / General Physician",
        "specialty_icon": "❤️",
        "suggestions": [
            "Monitor your blood pressure at home regularly.",
            "Follow a low-sodium (DASH) diet.",
            "Exercise for at least 150 minutes per week.",
            "Reduce stress through meditation, yoga, or deep breathing."
        ]
    },
    "Hyperthyroidism": {
        "specialty": "Endocrinologist",
        "specialty_icon": "🧬",
        "suggestions": [
            "Take prescribed antithyroid medications consistently.",
            "Avoid excessive iodine in diet (seaweed, iodized supplements).",
            "Monitor heart rate and bone density regularly.",
            "Discuss radioactive iodine therapy or surgery with your specialist."
        ]
    },
    "Hypoglycemia": {
        "specialty": "Endocrinologist",
        "specialty_icon": "🩸",
        "suggestions": [
            "Immediately consume 15g of fast-acting sugar (juice, glucose tablets).",
            "Carry a glucose source with you at all times.",
            "Eat regular meals and snacks; don't skip meals.",
            "Adjust insulin/medication doses with your doctor's guidance."
        ]
    },
    "Hypothyroidism": {
        "specialty": "Endocrinologist",
        "specialty_icon": "🧬",
        "suggestions": [
            "Take levothyroxine medication exactly as prescribed (empty stomach).",
            "Get regular TSH blood tests every 6–12 months.",
            "Eat a balanced diet; avoid excessive raw cruciferous vegetables.",
            "Regular exercise helps manage fatigue and weight gain."
        ]
    },
    "Impetigo": {
        "specialty": "Dermatologist / General Physician",
        "specialty_icon": "🧴",
        "suggestions": [
            "Apply prescribed antibiotic ointment to affected areas.",
            "Keep sores covered with a non-stick bandage.",
            "Wash hands frequently and don't touch or scratch sores.",
            "Avoid close contact with others until sores heal."
        ]
    },
    "Jaundice": {
        "specialty": "Gastroenterologist / Hepatologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Seek immediate medical evaluation to identify the underlying cause.",
            "Stay hydrated and eat a light diet.",
            "Avoid alcohol completely.",
            "Get liver function tests and an abdominal ultrasound."
        ]
    },
    "Malaria": {
        "specialty": "Infectious Disease Specialist",
        "specialty_icon": "🦠",
        "suggestions": [
            "Seek urgent medical care — antimalarial drugs are essential.",
            "Stay hydrated; fever can cause serious dehydration.",
            "Use mosquito nets and repellents to prevent reinfection.",
            "Complete the full course of prescribed antimalarial medication."
        ]
    },
    "Migraine": {
        "specialty": "Neurologist",
        "specialty_icon": "🧠",
        "suggestions": [
            "Rest in a dark, quiet room during a migraine attack.",
            "Apply cold or warm compress to your head or neck.",
            "Keep a migraine diary to identify personal triggers.",
            "Discuss preventive medications with your neurologist."
        ]
    },
    "Osteoarthristis": {
        "specialty": "Orthopedist / Rheumatologist",
        "specialty_icon": "🦴",
        "suggestions": [
            "Engage in low-impact exercise to maintain joint mobility.",
            "Maintain a healthy body weight to reduce joint load.",
            "Use heat or ice therapy for pain relief.",
            "Physical therapy can significantly improve function."
        ]
    },
    "Paralysis (brain hemorrhage)": {
        "specialty": "Neurologist / Neurosurgeon — SEEK EMERGENCY CARE",
        "specialty_icon": "🚨",
        "suggestions": [
            "Call emergency services (911) IMMEDIATELY.",
            "Do not give food or water — patient may have swallowing difficulties.",
            "Keep the patient calm and do not move them unnecessarily.",
            "Time is critical — early treatment significantly improves outcomes."
        ]
    },
    "Peptic ulcer diseae": {
        "specialty": "Gastroenterologist",
        "specialty_icon": "🫀",
        "suggestions": [
            "Take prescribed proton pump inhibitors (PPIs) consistently.",
            "Avoid NSAIDs (ibuprofen, aspirin) unless prescribed.",
            "Eat smaller, regular meals and avoid spicy/acidic foods.",
            "Get tested for H. pylori bacteria — treatment can cure the ulcer."
        ]
    },
    "Pneumonia": {
        "specialty": "Pulmonologist / General Physician",
        "specialty_icon": "🫁",
        "suggestions": [
            "Complete the full antibiotic course as prescribed.",
            "Rest well and stay hydrated.",
            "Use a humidifier to ease breathing.",
            "Seek emergency care if breathing worsens or oxygen levels drop."
        ]
    },
    "Psoriasis": {
        "specialty": "Dermatologist",
        "specialty_icon": "🧴",
        "suggestions": [
            "Moisturize skin regularly with fragrance-free lotions.",
            "Apply prescribed topical corticosteroids or vitamin D analogues.",
            "Avoid triggers: stress, smoking, skin injuries, certain medications.",
            "Phototherapy may be recommended for widespread psoriasis."
        ]
    },
    "Tuberculosis": {
        "specialty": "Pulmonologist / Infectious Disease Specialist",
        "specialty_icon": "🫁",
        "suggestions": [
            "Start and COMPLETE the full 6-month antibiotic course — do not stop early.",
            "Isolate yourself initially to prevent spreading TB.",
            "Ensure close contacts are screened for TB.",
            "Eat a nutritious, high-protein diet to support recovery."
        ]
    },
    "Typhoid": {
        "specialty": "Infectious Disease Specialist / General Physician",
        "specialty_icon": "🦠",
        "suggestions": [
            "Take prescribed antibiotics for the complete course.",
            "Drink only boiled or safe bottled water.",
            "Eat light, easily digestible foods.",
            "Maintain strict hygiene — wash hands frequently."
        ]
    },
    "Urinary tract infection": {
        "specialty": "Urologist / General Physician",
        "specialty_icon": "🧬",
        "suggestions": [
            "Drink plenty of water to flush out bacteria.",
            "Complete the prescribed antibiotic course fully.",
            "Avoid holding urine — urinate when you need to.",
            "After sex, urinate promptly to prevent recurrence."
        ]
    },
    "Varicose veins": {
        "specialty": "Vascular Surgeon",
        "specialty_icon": "🩸",
        "suggestions": [
            "Wear prescribed compression stockings.",
            "Elevate your legs when resting.",
            "Exercise regularly — walking helps circulation.",
            "Avoid prolonged standing or sitting."
        ]
    },
    "hepatitis A": {
        "specialty": "Gastroenterologist / General Physician",
        "specialty_icon": "🫀",
        "suggestions": [
            "Rest well; most cases resolve on their own with supportive care.",
            "Stay well hydrated and eat small, light meals.",
            "Avoid alcohol completely during recovery.",
            "Get vaccinated against hepatitis A to prevent future infection."
        ]
    },
}

DEFAULT_INFO = {
    "specialty": "General Physician",
    "specialty_icon": "🩺",
    "suggestions": [
        "Consult a general physician for proper evaluation.",
        "Keep a record of your symptoms (duration, severity, triggers).",
        "Rest well and stay hydrated.",
        "Do not self-medicate — seek professional advice."
    ]
}


def get_disease_info(disease_name):
    """Return specialty & suggestions for a disease, with a safe default."""
    disease_clean = disease_name.strip()
    if disease_clean in DISEASE_INFO:
        return DISEASE_INFO[disease_clean]
    # Fuzzy fallback: partial match
    for key in DISEASE_INFO:
        if disease_clean.lower() in key.lower() or key.lower() in disease_clean.lower():
            return DISEASE_INFO[key]
    return DEFAULT_INFO


# ── Symptom text matching ─────────────────────────────────────────────
def extract_symptoms_from_text(text):
    text_lower = text.lower()
    matched = {}
    for symptom in symptoms:
        readable = symptom.replace("_", " ").strip().lower()
        if readable in text_lower or re.search(r'\b' + re.escape(readable), text_lower):
            matched[symptom] = 1
        else:
            matched[symptom] = 0
    return matched


# ── Route: List all symptoms ──────────────────────────────────────────
@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    readable = [s.replace("_", " ").strip().title() for s in symptoms]
    return jsonify({"symptoms": symptoms, "readable": readable})


# ── Route: Predict from free text ────────────────────────────────────
@app.route("/predict/text", methods=["POST"])
def predict_from_text():
    data = request.json
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    input_data = extract_symptoms_from_text(text)
    matched_symptoms = [s for s, v in input_data.items() if v == 1]

    if not matched_symptoms:
        return jsonify({
            "prediction": None,
            "matched_symptoms": [],
            "confidence": 0,
            "message": "No recognizable symptoms found. Please describe your symptoms more specifically."
        })

    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    proba      = model.predict_proba(df)[0]
    confidence = round(float(max(proba)) * 100, 1)
    classes    = model.classes_

    top_indices = proba.argsort()[::-1][:3]
    top_predictions = [
        {"disease": classes[i], "confidence": round(float(proba[i]) * 100, 1)}
        for i in top_indices if proba[i] > 0.01
    ]

    readable_matched = [s.replace("_", " ").strip().title() for s in matched_symptoms]
    info = get_disease_info(prediction)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "matched_symptoms": readable_matched,
        "top_predictions": top_predictions,
        "recommended_specialty": info["specialty"],
        "specialty_icon": info["specialty_icon"],
        "health_suggestions": info["suggestions"],
        "message": "Prediction successful"
    })


# ── Route: Predict from symptom dict ─────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    data       = request.json
    input_data = {symptom: data.get(symptom, 0) for symptom in symptoms}
    df         = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    proba      = model.predict_proba(df)[0]
    confidence = round(float(max(proba)) * 100, 1)
    classes    = model.classes_

    top_indices = proba.argsort()[::-1][:3]
    top_predictions = [
        {"disease": classes[i], "confidence": round(float(proba[i]) * 100, 1)}
        for i in top_indices if proba[i] > 0.01
    ]

    info = get_disease_info(prediction)

    return jsonify({
        "prediction": prediction,
        "confidence": confidence,
        "top_predictions": top_predictions,
        "recommended_specialty": info["specialty"],
        "specialty_icon": info["specialty_icon"],
        "health_suggestions": info["suggestions"]
    })


# ── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)