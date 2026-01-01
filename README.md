# 🌾 Smart Irrigation & Farm Advisory System

A deterministic, rule-based agricultural decision support system built with Streamlit.

## 🚀 Quick Start

To run this application:

```bash
pip install streamlit
streamlit run app.py
```

Or install all dependencies:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🎯 Problem Statement

Indian farmers face critical challenges:
- **Water Mismanagement**: Over 60% of agriculture depends on unpredictable monsoons
- **Fertilizer Inefficiency**: Incorrect NPK application leading to soil degradation
- **Yield Uncertainty**: Inability to predict crop output for financial planning
- **Technology Gap**: Complex solutions not reaching small farmers

## ✨ Features

### 1. 💧 Smart Irrigation Module
- Analyzes soil moisture, weather, and crop requirements
- Provides precise irrigation recommendations
- Calculates water amount (mm) and duration
- Warns against over-irrigation
- **Rule-based logic**: Not AI guessing, pure mathematics

### 2. 🧪 Fertilizer Recommendation
- NPK recommendations based on crop, soil, and growth stage
- Split application timing guidance
- Organic fertilizer alternatives
- Seasonal total and stage-specific dosing

### 3. 📈 Yield Estimator
- Predicts crop yield based on water availability
- Considers rainfall and irrigation levels
- Provides cost vs benefit analysis
- Shows expected yield ranges with explanations

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Access the app** in your browser (typically opens automatically at `http://localhost:8501`)

## 📁 Project Structure

```
agriculture/
│
├── app.py                 # Main application with navigation
├── irrigation.py          # Smart irrigation module
├── fertilizer.py          # Fertilizer recommendation module
├── yield_estimator.py     # Yield estimation module
├── utils.py               # Utility functions and data
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎮 How to Use

1. **Launch the app** using `streamlit run app.py`
2. **Navigate** using the sidebar to select a module
3. **Enter your data**:
   - Crop type
   - Soil type
   - Current conditions (moisture, temperature, etc.)
4. **Click "Analyze"** or "Get Recommendation"
5. **Review results** and read the detailed explanations

## 🧮 Logic & Methodology

### Smart Irrigation Logic
```
IF moisture < 30% AND no rain expected
    → Irrigation REQUIRED
    
IF moisture > 60%
    → WARN over-irrigation
    
IF rain forecast > 40mm
    → DELAY irrigation
```

All calculations are:
- ✅ Deterministic (same inputs = same outputs)
- ✅ Based on soil science and crop requirements
- ✅ Transparent and explainable
- ❌ NOT based on AI/ML models
- ❌ NO hallucinations or predictions

## 📊 Sample Use Cases

### Scenario 1: Rice Farmer in Clay Soil
- **Input**: Rice crop, Clay soil, 25% moisture, 32°C, 10mm rain forecast
- **Output**: Irrigation needed, 45mm water, 4.5 hours duration
- **Reason**: Moisture below optimal, high temperature increases evaporation

### Scenario 2: Wheat in Vegetative Stage
- **Input**: Wheat, Loamy soil, Vegetative growth stage
- **Output**: NPK 40-15-9 kg/acre for current stage
- **Reason**: Stage needs 40% of total N, 30% of P, 30% of K

## 🔧 Customization

### Add New Crops
Edit [utils.py](utils.py):
```python
def get_crop_list():
    return ["Rice", "Wheat", "Your New Crop"]
```

### Modify NPK Values
Edit [fertilizer.py](fertilizer.py):
```python
crop_npk_base = {
    "Your Crop": {"N": 100, "P": 50, "K": 40}
}
```

## ⚠️ Disclaimer

This is a **prototype demonstration system**. While based on scientific principles:
- Values are placeholder estimates
- Should be validated with local agricultural experts
- Regional variations not fully accounted for
- Always consult agronomists for critical decisions

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Language**: Python 3.8+
- **Libraries**: pandas, numpy
- **Logic**: Pure deterministic rules (no ML/AI)

## 📝 License

This is an educational prototype for hackathon/demonstration purposes.

## 👨‍💻 Developer Notes

**Key Principles Followed**:
1. Math decides, explanation describes
2. No AI hallucinations - only deterministic calculations
3. Modular, clean code structure
4. User-friendly interface with clear explanations
5. Placeholder data clearly marked

## 🤝 Contributing

This is a prototype. To improve:
1. Add region-specific data
2. Integrate real weather APIs
3. Add more crops and soil types
4. Implement local language support
5. Add soil testing recommendations

---

**Built with ❤️ for Indian Agriculture** 🇮🇳
