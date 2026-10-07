# ⚡ AI Electrical Fault Diagnosis

An AI-powered electrical fault diagnosis system that uses machine learning to identify possible electrical faults from basic electrical measurements and an LLM to explain the result in simple language.

## 📌 Project Overview

This project takes electrical readings such as voltage, current, frequency, power factor, and temperature.

A Random Forest machine learning model analyzes these readings and predicts a possible electrical fault. An LLM then explains the prediction and suggests what an electrical worker should check.

**Electrical readings → ML prediction → Confidence score → LLM explanation**

> This project is designed as a decision-support system. It does not replace inspection or professional electrical diagnosis.

## 🧠 Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Random Forest Classifier
* Groq LLM
* Streamlit
* Joblib
* Pytest

## 📊 Dataset & Model

The model was trained on a balanced dataset containing **1,000 electrical readings** across five fault classes:

* Normal
* Overload
* Overvoltage
* Undervoltage
* Phase Imbalance

### Model Performance

**Test Accuracy: 95%**

The dataset was generated for this project to provide balanced examples for the five fault categories.

## ✨ Features

* Electrical fault prediction
* Model confidence score
* AI-generated fault explanation
* Practical suggested checks
* Streamlit web interface
* Balanced dataset
* Automated tests
* Local trained model
* Environment variable protection for API keys

## 🖥️ How It Works

```text
Electrical Readings
        ↓
Machine Learning Model
        ↓
Fault Prediction
        ↓
Confidence Score
        ↓
LLM Explanation
        ↓
Suggested Checks
```

## 📁 Project Structure

```text
AI_Electrical_Fault_Diagnosis/
│
├── app/
│   ├── __init__.py
│   ├── ui.py
│   └── services/
│       ├── fault_detector.py
│       └── llm_service.py
│
├── data/
│   └── electrical_data.csv
│
├── models/
│
├── tests/
│   └── test_fault_detector.py
│
├── generate_dataset.py
├── main.py
├── test_prediction.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Setup

Clone the repository and open the project folder.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## 🔑 Groq API Key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

## ▶️ Run the Application

First train the model:

```bash
python main.py
```

Then start the Streamlit application:

```bash
streamlit run app/ui.py
```

The application will open locally in your browser.

## 🧪 Run Tests

Run:

```bash
pytest
```

Current test result:

```text
2 passed
```

The tests verify electrical fault predictions for example normal and overvoltage readings.

## 🎯 Example

Input:

```text
Voltage: 255 V
Current: 4 A
Frequency: 50 Hz
Power Factor: 0.90
Temperature: 40 °C
```

Example result:

```text
Detected Fault: Overvoltage
Model Confidence: 99%
```

The LLM then provides a simple explanation of the possible fault and suggested checks.

## ⚠️ Disclaimer

This system is an educational and decision-support project. Predictions should not be treated as confirmed electrical diagnoses. Electrical equipment should be inspected by a qualified professional.

## 👩‍💻 Author

** Wajiha Gul**

BS Artificial Intelligence Student

UET Peshawar
