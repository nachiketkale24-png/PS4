"""
Smart Irrigation & Farm Advisory System
Main application file with navigation and home page
"""

import streamlit as st
from irrigation import show_irrigation_module
from irrigation_dashboard import show_irrigation_dashboard
from fertilizer import show_fertilizer_module
from yield_estimator import show_yield_estimator
from soil_detector import show_soil_detector

# Page configuration
st.set_page_config(
    page_title="Smart Farm Advisory",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 8px;
    }
    .problem-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

def show_home_page():
    """Display the home page"""
    
    # Main header
    st.markdown('<div class="main-header">🌾 Smart Irrigation & Farm Advisory</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Agricultural Decision Support System</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Problem statement section
    st.markdown("""
        <div class="problem-card">
            <h2>🎯 Problem Statement</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Indian farmers face critical challenges in optimizing water usage and crop management. 
                <strong>Over 60% of agriculture depends on monsoon</strong>, leading to unpredictable yields and income.
            </p>
            <h3>Key Challenges:</h3>
            <ul style="font-size: 1.05rem;">
                <li>💧 <strong>Water Mismanagement</strong>: Over-irrigation or under-irrigation due to lack of precise data</li>
                <li>🌱 <strong>Fertilizer Inefficiency</strong>: Incorrect NPK application causing soil degradation</li>
                <li>📉 <strong>Yield Uncertainty</strong>: Inability to predict crop output for financial planning</li>
                <li>📱 <strong>Limited Access to Technology</strong>: Complex agricultural solutions not reaching small farmers</li>
            </ul>
            <p style="font-size: 1.1rem; margin-top: 15px;">
                <strong>Our Solution</strong>: A simple, rule-based decision support system that provides 
                actionable recommendations based on scientific principles, not AI guesswork.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features overview
    st.markdown("## 🚀 Our Advisory Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>🔬 Soil Detector</h3>
                <p>AI-powered soil type identification:</p>
                <ul>
                    <li>Upload soil image</li>
                    <li>Instant soil type detection</li>
                    <li>Confidence meter</li>
                    <li>Soil characteristics</li>
                </ul>
                <p><strong>Output</strong>: Soil type and recommendations</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h3>🧪 Fertilizer Advisory</h3>
                <p>Optimize nutrient application with:</p>
                <ul>
                    <li>NPK recommendations</li>
                    <li>Growth stage-specific dosing</li>
                    <li>Split application timing</li>
                    <li>Organic alternatives</li>
                </ul>
                <p><strong>Output</strong>: Customized fertilizer schedule</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <h3>💧 Smart Irrigation</h3>
                <p>Get precise irrigation recommendations based on:</p>
                <ul>
                    <li>Soil moisture levels</li>
                    <li>Weather forecasts</li>
                    <li>Crop water needs</li>
                    <li>Soil type characteristics</li>
                </ul>
                <p><strong>Output</strong>: Water amount, duration, and timing</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <h3>📈 Yield Estimator</h3>
                <p>Predict crop output based on:</p>
                <ul>
                    <li>Water availability</li>
                    <li>Irrigation levels</li>
                    <li>Rainfall patterns</li>
                    <li>Crop type</li>
                </ul>
                <p><strong>Output</strong>: Yield range and profitability</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Why Trust Us section
    st.markdown("## ✅ Why Trust Our System?")
    
    trust_col1, trust_col2 = st.columns(2)
    
    with trust_col1:
        st.success("""
        **📐 Mathematical, Not Magical**
        - All recommendations based on established agricultural science
        - Deterministic rules, not AI hallucinations
        - Transparent calculations you can verify
        """)
        
        st.info("""
        **🌱 Farmer-Friendly**
        - Simple inputs that farmers already know
        - Clear explanations in plain language
        - Practical, actionable outputs
        """)
    
    with trust_col2:
        st.warning("""
        **🔬 Science-Backed**
        - Based on soil science principles
        - Uses crop-specific water requirements
        - Considers local environmental factors
        """)
        
        st.success("""
        **💰 Cost-Effective**
        - Reduce water wastage
        - Optimize fertilizer use
        - Improve yield predictions
        """)
    
    st.markdown("---")
    
    # Call to action
    st.markdown("## 🎯 Get Started Now!")
    
    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    
    with cta_col2:
        st.info("""
        ### 👈 Use the sidebar to navigate:
        - **🏠 Home**: You are here!
        - **� Soil Detector**: Identify soil type from image
        - **�💧 Smart Irrigation**: Get water recommendations
        - **🧪 Fertilizer Advisory**: Optimize nutrient application
        - **📈 Yield Estimator**: Predict crop output
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>🌾 <strong>Smart Irrigation & Farm Advisory System</strong></p>
            <p>Empowering farmers with data-driven decisions | Built with ❤️ for Indian Agriculture</p>
            <p style="font-size: 0.9rem;">Note: This is a prototype system. Always consult local agricultural experts for critical decisions.</p>
        </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Sidebar navigation
    st.sidebar.title("🌾 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Module:",
        ["🏠 Home", "🔬 Soil Detector", "💧 Smart Irrigation", "🎯 Irrigation Dashboard", "🧪 Fertilizer Advisory", "📈 Yield Estimator"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info("""
    This system provides:
    - **Deterministic** calculations
    - **Rule-based** recommendations
    - **Science-backed** advice
    
    Not AI predictions, but mathematical precision.
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Quick Tips")
    st.sidebar.success("""
    1. Select a module from above
    2. Enter your field data
    3. Get instant recommendations
    4. Read the explanations
    """)
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "� Soil Detector":
        show_soil_detector()
    elif page == "�💧 Smart Irrigation":
        show_irrigation_module()    elif page == "🎯 Irrigation Dashboard":
        show_irrigation_dashboard()    elif page == "🧪 Fertilizer Advisory":
        show_fertilizer_module()
    elif page == "📈 Yield Estimator":
        show_yield_estimator()

if __name__ == "__main__":
    main()
