"""
Smart Irrigation Module
Deterministic rule-based irrigation recommendation system
"""

import streamlit as st
from utils import get_crop_list, get_soil_types, get_soil_water_capacity, get_crop_water_requirement

def calculate_irrigation_need(crop_type, soil_type, moisture, temperature, rain_forecast):
    """
    Calculate irrigation requirements based on deterministic rules
    
    Returns: dict with irrigation decision, water amount, duration, and explanation
    """
    soil_capacity = get_soil_water_capacity(soil_type)
    crop_water_req = get_crop_water_requirement(crop_type)
    
    # Decision variables
    needs_irrigation = False
    water_amount_mm = 0
    warning = None
    explanation_parts = []
    
    # Rule 1: Check soil moisture levels
    if moisture < soil_capacity["low"]:
        explanation_parts.append(f"🔴 Current soil moisture ({moisture}%) is critically low (below {soil_capacity['low']}%).")
        needs_irrigation = True
        moisture_deficit = soil_capacity["optimal_min"] - moisture
    elif moisture < soil_capacity["optimal_min"]:
        explanation_parts.append(f"🟡 Current soil moisture ({moisture}%) is below optimal range ({soil_capacity['optimal_min']}-{soil_capacity['optimal_max']}%).")
        needs_irrigation = True
        moisture_deficit = soil_capacity["optimal_min"] - moisture
    elif moisture > soil_capacity["high"]:
        explanation_parts.append(f"⚠️ Warning: Soil moisture ({moisture}%) is too high (above {soil_capacity['high']}%). Risk of waterlogging and root rot.")
        warning = "OVER-IRRIGATION DETECTED"
        moisture_deficit = 0
    elif moisture > soil_capacity["optimal_max"]:
        explanation_parts.append(f"✅ Soil moisture ({moisture}%) is adequate but on the higher side. No irrigation needed.")
        moisture_deficit = 0
    else:
        explanation_parts.append(f"✅ Soil moisture ({moisture}%) is in optimal range ({soil_capacity['optimal_min']}-{soil_capacity['optimal_max']}%).")
        moisture_deficit = 0
    
    # Rule 2: Check rain forecast
    if rain_forecast > 40:
        explanation_parts.append(f"🌧️ Heavy rain expected ({rain_forecast}mm in next 3 days). Irrigation should be delayed.")
        if needs_irrigation:
            explanation_parts.append("💡 Although soil is dry, upcoming rain will likely fulfill water requirements.")
        needs_irrigation = False
        water_amount_mm = 0
    elif rain_forecast > 20:
        explanation_parts.append(f"🌦️ Moderate rain expected ({rain_forecast}mm in next 3 days).")
        if needs_irrigation:
            # Reduce irrigation amount accounting for expected rain
            moisture_deficit = max(0, moisture_deficit - (rain_forecast * 0.3))
            explanation_parts.append(f"💡 Irrigation amount reduced to account for expected rainfall.")
    elif rain_forecast > 0:
        explanation_parts.append(f"☁️ Light rain expected ({rain_forecast}mm in next 3 days).")
    else:
        explanation_parts.append("☀️ No rain expected in next 3 days.")
    
    # Rule 3: Calculate water amount if irrigation needed
    if needs_irrigation and not warning:
        # Base water amount on moisture deficit and crop requirements
        water_amount_mm = moisture_deficit * 0.8 + crop_water_req * 2
        water_amount_mm = round(water_amount_mm, 1)
        
        # Temperature adjustment
        if temperature > 35:
            temp_factor = 1.2
            explanation_parts.append(f"🌡️ High temperature ({temperature}°C) increases evaporation. Water requirement increased by 20%.")
        elif temperature > 30:
            temp_factor = 1.1
            explanation_parts.append(f"🌡️ Temperature ({temperature}°C) is high. Water requirement increased by 10%.")
        elif temperature < 15:
            temp_factor = 0.9
            explanation_parts.append(f"🌡️ Cool temperature ({temperature}°C) reduces evaporation. Water requirement decreased by 10%.")
        else:
            temp_factor = 1.0
            explanation_parts.append(f"🌡️ Temperature ({temperature}°C) is moderate.")
        
        water_amount_mm = round(water_amount_mm * temp_factor, 1)
        
        explanation_parts.append(f"💧 Recommended irrigation: {water_amount_mm}mm to bring soil to optimal moisture level.")
    
    # Calculate duration (assuming typical irrigation rate of 10mm/hour)
    irrigation_rate = 10  # mm/hour
    duration_hours = round(water_amount_mm / irrigation_rate, 2) if water_amount_mm > 0 else 0
    
    # Final recommendation
    if warning:
        recommendation = "⛔ DO NOT IRRIGATE - Soil is oversaturated"
    elif needs_irrigation:
        recommendation = "✅ IRRIGATION REQUIRED"
    else:
        recommendation = "⏸️ NO IRRIGATION NEEDED"
    
    return {
        "needs_irrigation": needs_irrigation and not warning,
        "recommendation": recommendation,
        "water_amount_mm": water_amount_mm,
        "duration_hours": duration_hours,
        "warning": warning,
        "explanation": "\n\n".join(explanation_parts),
        "crop_type": crop_type,
        "soil_type": soil_type
    }


def show_irrigation_module():
    """Display the Smart Irrigation Module UI"""
    st.header("🌾 Smart Irrigation Advisory")
    st.markdown("---")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Field Information")
        crop_type = st.selectbox("Crop Type", get_crop_list(), key="irr_crop")
        soil_type = st.selectbox("Soil Type", get_soil_types(), key="irr_soil")
        soil_moisture = st.slider("Current Soil Moisture (%)", 0, 100, 45, key="irr_moisture")
    
    with col2:
        st.subheader("🌤️ Weather Data")
        temperature = st.slider("Current Temperature (°C)", 10, 45, 28, key="irr_temp")
        rain_forecast = st.slider("Rain Forecast - Next 3 Days (mm)", 0, 100, 5, key="irr_rain")
    
    st.markdown("---")
    
    # Calculate button
    if st.button("🔍 Analyze Irrigation Need", type="primary", use_container_width=True):
        result = calculate_irrigation_need(
            crop_type, soil_type, soil_moisture, temperature, rain_forecast
        )
        
        # Display results in cards
        st.markdown("### 📊 Analysis Results")
        
        # Main recommendation card
        if result["warning"]:
            st.error(f"### {result['recommendation']}")
        elif result["needs_irrigation"]:
            st.success(f"### {result['recommendation']}")
        else:
            st.info(f"### {result['recommendation']}")
        
        # Results in columns
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                label="💧 Water Amount",
                value=f"{result['water_amount_mm']} mm",
                delta="Required" if result['needs_irrigation'] else "Not needed"
            )
        
        with metric_col2:
            st.metric(
                label="⏱️ Duration",
                value=f"{result['duration_hours']} hours",
                delta="Estimated" if result['needs_irrigation'] else "N/A"
            )
        
        with metric_col3:
            status_emoji = "🚫" if result['warning'] else ("✅" if result['needs_irrigation'] else "⏸️")
            st.metric(
                label="Status",
                value=status_emoji,
                delta=soil_type
            )
        
        # Detailed explanation
        st.markdown("### 📝 Detailed Explanation")
        with st.expander("View Analysis Details", expanded=True):
            st.markdown(result['explanation'])
            
            st.markdown("---")
            st.markdown("#### 🎯 How This Was Calculated")
            st.markdown(f"""
            - **Crop**: {result['crop_type']} requires approximately {get_crop_water_requirement(crop_type)} mm/day
            - **Soil Type**: {result['soil_type']} has specific water retention characteristics
            - **Decision Logic**: Based on soil moisture thresholds, weather conditions, and crop requirements
            - **Note**: This is a deterministic calculation, not AI prediction. The math decides, explanation describes why.
            """)
