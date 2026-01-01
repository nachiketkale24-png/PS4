"""
Farmer-Friendly Irrigation Dashboard
Clean, simple, visual interface for irrigation decisions
"""

import streamlit as st
from irrigation_controller import IrrigationController
from datetime import datetime, timedelta


# ============================================================================
# CONFIGURATION & TRANSLATIONS
# ============================================================================

TRANSLATIONS = {
    "en": {
        "title": "💧 Smart Irrigation Dashboard",
        "subtitle": "Simple water management for your farm",
        "input_section": "📝 Tell us about your field",
        "crop": "Crop Type",
        "soil": "Soil Type",
        "moisture": "Soil Moisture",
        "temperature": "Temperature",
        "rain_chance": "Rain Chance (Next 3 Days)",
        "stage": "Crop Growth Stage",
        "analyze": "Check Water Needs",
        "decision": "Irrigation Decision",
        "water_needed": "Water Needed",
        "duration": "Duration",
        "frequency": "Water Every",
        "method": "Method",
        "risks": "Alerts",
        "explain_why": "Why this decision?",
        "next_7_days": "7-Day Watering Plan",
        "yes": "Yes, Water Today",
        "no": "No, Skip Today",
        "days": "days",
        "minutes": "minutes",
        "mm": "mm",
        "celsius": "°C",
        "percent": "%",
        "good": "Good",
        "warning": "Warning",
        "critical": "Critical"
    },
    "hi": {
        "title": "💧 स्मार्ट सिंचाई डैशबोर्ड",
        "subtitle": "आपके खेत के लिए आसान पानी प्रबंधन",
        "input_section": "📝 अपने खेत के बारे में बताएं",
        "crop": "फसल का प्रकार",
        "soil": "मिट्टी का प्रकार",
        "moisture": "मिट्टी में नमी",
        "temperature": "तापमान",
        "rain_chance": "बारिश की संभावना (अगले 3 दिन)",
        "stage": "फसल की अवस्था",
        "analyze": "पानी की जरूरत जांचें",
        "decision": "सिंचाई का निर्णय",
        "water_needed": "पानी की जरूरत",
        "duration": "समय",
        "frequency": "पानी दें हर",
        "method": "तरीका",
        "risks": "चेतावनी",
        "explain_why": "यह निर्णय क्यों?",
        "next_7_days": "7-दिन की सिंचाई योजना",
        "yes": "हां, आज पानी दें",
        "no": "नहीं, आज छोड़ें",
        "days": "दिन",
        "minutes": "मिनट",
        "mm": "मिमी",
        "celsius": "°C",
        "percent": "%",
        "good": "अच्छा",
        "warning": "चेतावनी",
        "critical": "गंभीर"
    }
}

# Crop options with translations
CROPS = {
    "en": ["Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Potato", "Tomato", "Onion", "Groundnut"],
    "hi": ["धान", "गेहूं", "कपास", "मक्का", "गन्ना", "सोयाबीन", "आलू", "टमाटर", "प्याज", "मूंगफली"]
}

CROP_MAPPING = {
    "धान": "rice", "गेहूं": "wheat", "कपास": "cotton", "मक्का": "maize",
    "गन्ना": "sugarcane", "सोयाबीन": "soybean", "आलू": "potato",
    "टमाटर": "tomato", "प्याज": "onion", "मूंगफली": "groundnut"
}

SOILS = {
    "en": ["Clay", "Loam", "Sandy"],
    "hi": ["चिकनी मिट्टी", "दोमट", "रेतीली"]
}

SOIL_MAPPING = {
    "चिकनी मिट्टी": "clay", "दोमट": "loam", "रेतीली": "sandy"
}

STAGES = {
    "en": ["Germination", "Vegetative", "Flowering", "Harvest"],
    "hi": ["अंकुरण", "वृद्धि", "फूल", "कटाई"]
}

STAGE_MAPPING = {
    "अंकुरण": "germination", "वृद्धि": "vegetative", "फूल": "flowering", "कटाई": "harvest"
}


# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

def render_language_toggle():
    """
    Render language selection toggle
    Returns: Selected language code ('en' or 'hi')
    """
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col2:
        if st.button("🇬🇧 EN", use_container_width=True, 
                     type="primary" if st.session_state.get('language', 'en') == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    
    with col3:
        if st.button("🇮🇳 हि", use_container_width=True,
                     type="primary" if st.session_state.get('language', 'en') == 'hi' else "secondary"):
            st.session_state.language = 'hi'
            st.rerun()
    
    return st.session_state.get('language', 'en')


def render_metric_card(icon, title, value, subtitle, color="blue"):
    """
    Render a large, readable metric card
    
    Args:
        icon: Emoji icon
        title: Card title
        value: Main value to display
        subtitle: Additional context
        color: Card color theme (blue, green, orange, red)
    """
    color_map = {
        "blue": "#2196F3",
        "green": "#4CAF50",
        "orange": "#FF9800",
        "red": "#F44336",
        "gray": "#9E9E9E"
    }
    
    bg_color = color_map.get(color, color_map["blue"])
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {bg_color} 0%, {bg_color}DD 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
            <div style="font-size: 1.1rem; opacity: 0.9; margin-bottom: 5px;">{title}</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin: 10px 0;">{value}</div>
            <div style="font-size: 1rem; opacity: 0.85;">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)


def render_decision_card(need_irrigation, lang="en"):
    """
    Render main irrigation decision card with large visual indicator
    
    Args:
        need_irrigation: Boolean decision
        lang: Language code
    """
    t = TRANSLATIONS[lang]
    
    if need_irrigation:
        icon = "💧"
        decision_text = t["yes"]
        color = "#4CAF50"
        emoji_bg = "✅"
    else:
        icon = "⏸️"
        decision_text = t["no"]
        color = "#FF9800"
        emoji_bg = "⏹️"
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color} 0%, {color}DD 100%);
            padding: 40px;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            margin: 20px 0;
        ">
            <div style="font-size: 5rem; margin-bottom: 15px;">{emoji_bg}</div>
            <div style="font-size: 1.5rem; opacity: 0.9; margin-bottom: 10px;">{t['decision']}</div>
            <div style="font-size: 3rem; font-weight: bold; margin: 15px 0;">{decision_text}</div>
            <div style="font-size: 1.8rem;">{icon}</div>
        </div>
    """, unsafe_allow_html=True)


def render_water_bar(water_mm, max_water=50, lang="en"):
    """
    Render visual bar showing water amount needed
    
    Args:
        water_mm: Water amount in millimeters
        max_water: Maximum value for bar scale
        lang: Language code
    """
    t = TRANSLATIONS[lang]
    
    # Calculate percentage for progress bar
    percentage = min((water_mm / max_water) * 100, 100)
    
    # Color based on amount
    if water_mm == 0:
        bar_color = "#9E9E9E"
    elif water_mm < 10:
        bar_color = "#4CAF50"
    elif water_mm < 30:
        bar_color = "#FF9800"
    else:
        bar_color = "#F44336"
    
    st.markdown(f"### 💦 {t['water_needed']}")
    st.markdown(f"""
        <div style="
            background-color: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            height: 60px;
            position: relative;
            margin: 20px 0;
        ">
            <div style="
                background: linear-gradient(90deg, {bar_color} 0%, {bar_color}BB 100%);
                width: {percentage}%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.8rem;
                font-weight: bold;
                transition: width 0.5s ease;
            ">
                {water_mm} {t['mm']}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_risk_banner(risks, lang="en"):
    """
    Render color-coded risk alerts banner
    
    Args:
        risks: List of risk strings
        lang: Language code
    """
    t = TRANSLATIONS[lang]
    
    # Categorize risk level based on keywords
    critical_keywords = ["critical", "wilting", "extreme", "गंभीर"]
    warning_keywords = ["warning", "high", "below", "चेतावनी"]
    
    risk_text = " ".join(risks).lower()
    
    if any(keyword in risk_text for keyword in critical_keywords):
        alert_type = "error"
        icon = "🔴"
        level = t["critical"]
    elif any(keyword in risk_text for keyword in warning_keywords):
        alert_type = "warning"
        icon = "🟡"
        level = t["warning"]
    else:
        alert_type = "info"
        icon = "🟢"
        level = t["good"]
    
    st.markdown(f"### ⚠️ {t['risks']}")
    
    for risk in risks:
        if alert_type == "error":
            st.error(f"{icon} {risk}")
        elif alert_type == "warning":
            st.warning(f"{icon} {risk}")
        else:
            st.info(f"{icon} {risk}")


def render_7day_timeline(frequency_days, need_irrigation, lang="en"):
    """
    Render 7-day irrigation timeline/plan
    
    Args:
        frequency_days: Days between irrigation
        need_irrigation: Whether irrigation is needed today
        lang: Language code
    """
    t = TRANSLATIONS[lang]
    
    st.markdown(f"### 📅 {t['next_7_days']}")
    
    # Create timeline for next 7 days
    today = datetime.now()
    timeline_html = '<div style="display: flex; gap: 10px; overflow-x: auto; padding: 20px 0;">'
    
    for i in range(7):
        date = today + timedelta(days=i)
        day_name = date.strftime("%a")
        day_num = date.strftime("%d")
        
        # Determine if irrigation needed on this day
        if i == 0 and need_irrigation:
            should_irrigate = True
        elif frequency_days > 0 and i % frequency_days == 0 and need_irrigation:
            should_irrigate = True
        else:
            should_irrigate = False
        
        # Set colors
        if should_irrigate:
            bg_color = "#4CAF50"
            icon = "💧"
            text = "Water" if lang == "en" else "पानी दें"
        else:
            bg_color = "#E0E0E0"
            icon = "—"
            text = "Skip" if lang == "en" else "छोड़ें"
            color = "#666"
        
        timeline_html += f"""
            <div style="
                flex: 1;
                min-width: 100px;
                background-color: {bg_color};
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                color: {'white' if should_irrigate else '#666'};
            ">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-weight: bold; font-size: 1.2rem; margin: 5px 0;">{day_name}</div>
                <div style="font-size: 0.9rem;">{day_num}</div>
                <div style="font-size: 0.8rem; margin-top: 5px;">{text}</div>
            </div>
        """
    
    timeline_html += '</div>'
    st.markdown(timeline_html, unsafe_allow_html=True)


# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def show_irrigation_dashboard():
    """
    Main irrigation dashboard with farmer-friendly interface
    """
    # Language selection
    lang = render_language_toggle()
    t = TRANSLATIONS[lang]
    
    # Header
    st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 3rem; color: #2E7D32; margin-bottom: 10px;">
                {t['title']}
            </h1>
            <p style="font-size: 1.3rem; color: #666;">
                {t['subtitle']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input Section - Simple and clean
    st.markdown(f"## {t['input_section']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Crop selection
        crop_display = st.selectbox(
            f"🌾 {t['crop']}", 
            CROPS[lang],
            key="dash_crop"
        )
        crop_name = CROP_MAPPING.get(crop_display, crop_display.lower())
        
        # Soil type
        soil_display = st.selectbox(
            f"🏞️ {t['soil']}", 
            SOILS[lang],
            key="dash_soil"
        )
        soil_type = SOIL_MAPPING.get(soil_display, soil_display.lower())
        
        # Moisture slider with large text
        st.markdown(f"**💧 {t['moisture']}**")
        moisture = st.slider(
            "",
            0, 100, 35,
            key="dash_moisture",
            help="Current water level in soil"
        )
        st.markdown(f"<p style='font-size: 1.5rem; text-align: center;'><b>{moisture}{t['percent']}</b></p>", 
                   unsafe_allow_html=True)
    
    with col2:
        # Temperature
        st.markdown(f"**🌡️ {t['temperature']}**")
        temperature = st.slider(
            "",
            10, 45, 28,
            key="dash_temp"
        )
        st.markdown(f"<p style='font-size: 1.5rem; text-align: center;'><b>{temperature}{t['celsius']}</b></p>", 
                   unsafe_allow_html=True)
        
        # Rain probability
        st.markdown(f"**🌧️ {t['rain_chance']}**")
        rain_prob = st.slider(
            "",
            0, 100, 20,
            key="dash_rain"
        )
        st.markdown(f"<p style='font-size: 1.5rem; text-align: center;'><b>{rain_prob}{t['percent']}</b></p>", 
                   unsafe_allow_html=True)
        
        # Growth stage
        stage_display = st.selectbox(
            f"🌱 {t['stage']}", 
            STAGES[lang],
            key="dash_stage"
        )
        stage = STAGE_MAPPING.get(stage_display, stage_display.lower())
    
    st.markdown("---")
    
    # Large analyze button
    if st.button(f"🔍 {t['analyze']}", type="primary", use_container_width=True):
        # Get decision from controller
        controller = IrrigationController()
        result = controller.calculate_irrigation_decision(
            soil_type=soil_type,
            crop_name=crop_name,
            current_soil_moisture=moisture,
            temperature=temperature,
            rainfall_probability=rain_prob,
            crop_stage=stage
        )
        
        # Store in session state
        st.session_state.irrigation_result = result
    
    # Display results if available
    if 'irrigation_result' in st.session_state:
        result = st.session_state.irrigation_result
        
        st.markdown("---")
        st.markdown("## 📊 Your Irrigation Plan")
        
        # Main decision card
        render_decision_card(result['need_irrigation'], lang)
        
        # Metrics cards in grid
        st.markdown("### 📋 Details")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            render_metric_card(
                "💦",
                t['water_needed'],
                f"{result['water_required_mm']} {t['mm']}",
                t['water_needed'],
                "blue" if result['need_irrigation'] else "gray"
            )
        
        with metric_col2:
            render_metric_card(
                "⏱️",
                t['duration'],
                f"{result['recommended_duration_minutes']}",
                t['minutes'],
                "green" if result['need_irrigation'] else "gray"
            )
        
        with metric_col3:
            render_metric_card(
                "🔄",
                t['frequency'],
                f"{result['frequency_days']}",
                t['days'],
                "orange"
            )
        
        with metric_col4:
            render_metric_card(
                "🚿",
                t['method'],
                result['irrigation_method'].title(),
                "",
                "blue"
            )
        
        st.markdown("---")
        
        # Water visualization bar
        render_water_bar(result['water_required_mm'], lang=lang)
        
        st.markdown("---")
        
        # Risk alerts
        render_risk_banner(result['risks'], lang)
        
        st.markdown("---")
        
        # 7-day timeline
        render_7day_timeline(
            result['frequency_days'],
            result['need_irrigation'],
            lang
        )
        
        st.markdown("---")
        
        # Expandable explanation
        with st.expander(f"💡 {t['explain_why']}", expanded=False):
            st.markdown(f"""
                <div style="
                    background-color: #FFF9C4;
                    padding: 20px;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    line-height: 1.8;
                    color: #333;
                ">
                    {result['explanation']}
                </div>
            """, unsafe_allow_html=True)


# For standalone testing
if __name__ == "__main__":
    st.set_page_config(
        page_title="Irrigation Dashboard",
        page_icon="💧",
        layout="wide"
    )
    show_irrigation_dashboard()
