# AI-Powered Symptom Analysis & Disease Prediction System

## Overview
This is a full-stack AI-driven healthcare microservice designed to analyze user symptoms and provide preliminary disease predictions along with medical recommendations.

## Tech Stack
- **Backend:** Python (Flask)
- **Machine Learning:** Scikit-Learn (Random Forest), Pandas, NumPy
- **Frontend:** Responsive Vanilla JavaScript, HTML5, CSS3 (Glassmorphic Design)
- **Deployment:** Docker

## Key Features
- **Symptom-Based Prediction:** Analyzes 130+ clinical symptoms to predict 40+ unique conditions.
- **Natural Language Input:** Uses NLP/Regex matching to extract symptoms from plain-text descriptions.
- **Medical Recommendations:** Suggests doctor specialties (e.g., Cardiologist, Neurologist) and provides actionable health advice.
- **Confidence Scoring:** Displays model confidence for each prediction.
- **Interactive UI:** A modern, mobile-friendly interface for symptom tracking.

## Getting Started

### Local Setup
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Backend:**
   ```bash
   python src/app.py
   ```
3. **Open the Frontend:**
   Open `frontend/index.html` in your browser.

### Docker Setup
1. **Build Image:**
   ```bash
   docker build -t ai-symptom-service .
   ```
2. **Run Container:**
   ```bash
   docker run -p 5000:5000 ai-symptom-service
   ```

## Project Structure
- `src/`: Backend API and training scripts.
- `frontend/`: UI files.
- `model/`: Pre-trained ML models (Pickle format).
- `dataset/`: Training and testing data.

## Disclaimer
*This tool provides preliminary suggestions for informational purposes only. It is NOT a substitute for professional medical advice.*
