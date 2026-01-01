"""
Soil Detector Module
Image-based soil type detection (currently simulated, will use MobileNetV2 later)
"""

import streamlit as st
from PIL import Image
import io

def simulate_soil_prediction(image_file):
    """
    Simulate soil type prediction based on file size
    TODO: Replace with actual MobileNetV2 model later
    
    Args:
        image_file: Uploaded image file
    
    Returns:
        dict with predicted soil type and confidence
    """
    # Get file size in bytes
    file_size = len(image_file.getvalue())
    file_size_kb = file_size / 1024
    
    # Simulate prediction based on file size
    # Small files → Sandy (lighter colors, less detail)
    # Medium files → Loamy (balanced)
    # Large files → Clay (darker, more detail)
    
    if file_size_kb < 50:
        soil_type = "Sandy"
        confidence = 78.5
        color = "#F4A460"  # Sandy brown
        characteristics = [
            "Light colored soil",
            "Loose texture",
            "Poor water retention",
            "Good drainage"
        ]
        recommendation = "Sandy soil drains quickly. Consider adding organic matter and water more frequently."
    elif file_size_kb < 150:
        soil_type = "Loamy"
        confidence = 85.2
        color = "#8B4513"  # Saddle brown
        characteristics = [
            "Balanced texture",
            "Dark brown color",
            "Good water retention",
            "Excellent for farming"
        ]
        recommendation = "Loamy soil is ideal for most crops. Maintain organic content with compost."
    elif file_size_kb < 300:
        soil_type = "Silty"
        confidence = 72.8
        color = "#A0522D"  # Sienna
        characteristics = [
            "Smooth texture",
            "Medium brown color",
            "Moderate water retention",
            "Can become compact"
        ]
        recommendation = "Silty soil holds nutrients well but may compact. Avoid over-tilling."
    else:
        soil_type = "Clay"
        confidence = 81.3
        color = "#654321"  # Dark brown
        characteristics = [
            "Heavy texture",
            "Dark colored",
            "High water retention",
            "Can become waterlogged"
        ]
        recommendation = "Clay soil retains water well but drains slowly. Add sand or organic matter to improve drainage."
    
    # Add some variation to make it look realistic
    import random
    confidence += random.uniform(-3, 3)
    confidence = round(min(max(confidence, 65), 95), 1)
    
    # Generate secondary predictions (less confident)
    all_soils = ["Sandy", "Loamy", "Clay", "Silty", "Peaty", "Chalky"]
    secondary_predictions = []
    remaining = 100 - confidence
    
    for soil in all_soils:
        if soil != soil_type:
            sec_conf = random.uniform(5, remaining/3)
            secondary_predictions.append({"soil": soil, "confidence": round(sec_conf, 1)})
            remaining -= sec_conf
            if len(secondary_predictions) >= 2:
                break
    
    return {
        "soil_type": soil_type,
        "confidence": confidence,
        "color": color,
        "characteristics": characteristics,
        "recommendation": recommendation,
        "secondary_predictions": secondary_predictions,
        "file_size_kb": round(file_size_kb, 2)
    }


def show_soil_detector():
    """Display the Soil Detector Module UI"""
    st.header("🔬 AI Soil Type Detector")
    st.markdown("---")
    
    # Information section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📸 Upload Soil Image for Analysis
        
        Take a clear photo of your soil sample and upload it here. Our AI system will analyze 
        the image to identify the soil type.
        
        **Tips for best results:**
        - Take photo in good lighting (natural daylight is best)
        - Clear close-up of the soil
        - Remove debris, stones, or grass from sample
        - Slightly moist soil shows better texture
        """)
    
    with col2:
        st.info("""
        **Supported Formats:**
        - JPG / JPEG
        - PNG
        - BMP
        
        **Max Size:** 10MB
        """)
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a soil image...",
        type=["jpg", "jpeg", "png", "bmp"],
        help="Upload a clear image of your soil sample"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col_img, col_analysis = st.columns([1, 1])
        
        with col_img:
            st.markdown("### 📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, caption="Your Soil Sample")
            
            # Image info
            st.caption(f"📏 Size: {image.size[0]} × {image.size[1]} pixels")
            st.caption(f"📦 File size: {len(uploaded_file.getvalue()) / 1024:.2f} KB")
        
        with col_analysis:
            st.markdown("### 🤖 AI Analysis")
            
            # Simulate analysis with progress bar
            with st.spinner("Analyzing soil type..."):
                import time
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)
                
                # Get prediction
                prediction = simulate_soil_prediction(uploaded_file)
            
            st.success("✅ Analysis Complete!")
        
        st.markdown("---")
        
        # Results section
        st.markdown("## 📊 Detection Results")
        
        # Main prediction
        result_col1, result_col2 = st.columns([2, 1])
        
        with result_col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {prediction['color']} 0%, #2C3E50 100%); 
                        padding: 30px; border-radius: 15px; color: white; text-align: center;">
                <h1 style="margin: 0; font-size: 3rem;">🏆 {prediction['soil_type']} Soil</h1>
                <p style="font-size: 1.5rem; margin-top: 10px;">Detected with {prediction['confidence']}% confidence</p>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col2:
            st.metric(
                label="Primary Prediction",
                value=prediction['soil_type'],
                delta=f"{prediction['confidence']}% confident"
            )
        
        st.markdown("---")
        
        # Confidence meter
        st.markdown("### 📈 Confidence Levels")
        
        # Main prediction confidence bar
        st.markdown(f"**{prediction['soil_type']} Soil**")
        st.progress(prediction['confidence'] / 100)
        st.caption(f"Confidence: {prediction['confidence']}%")
        
        # Secondary predictions
        if prediction['secondary_predictions']:
            st.markdown("**Other Possibilities:**")
            for sec_pred in prediction['secondary_predictions']:
                st.markdown(f"*{sec_pred['soil']} Soil*")
                st.progress(sec_pred['confidence'] / 100)
                st.caption(f"Confidence: {sec_pred['confidence']}%")
        
        st.markdown("---")
        
        # Soil characteristics
        st.markdown("### 🌱 Soil Characteristics")
        
        char_col1, char_col2 = st.columns(2)
        
        with char_col1:
            st.markdown("**Identified Features:**")
            for char in prediction['characteristics']:
                st.markdown(f"✓ {char}")
        
        with char_col2:
            st.markdown("**Color Sample:**")
            st.markdown(f"""
            <div style="width: 100%; height: 100px; background-color: {prediction['color']}; 
                        border-radius: 10px; border: 2px solid #ccc;"></div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendation
        st.markdown("### 💡 Farming Recommendations")
        st.info(f"**{prediction['recommendation']}**")
        
        # Additional tips based on soil type
        if prediction['soil_type'] == "Sandy":
            st.warning("""
            **Additional Tips for Sandy Soil:**
            - Water more frequently (low retention)
            - Add compost or manure regularly
            - Use mulching to reduce water loss
            - Choose drought-resistant crops
            """)
        elif prediction['soil_type'] == "Clay":
            st.warning("""
            **Additional Tips for Clay Soil:**
            - Ensure proper drainage
            - Avoid over-watering
            - Add organic matter to improve structure
            - Wait for soil to dry before tilling
            """)
        elif prediction['soil_type'] == "Loamy":
            st.success("""
            **Excellent Choice! Loamy Soil Tips:**
            - Maintain organic matter levels
            - Regular composting
            - Suitable for most crops
            - Balanced watering schedule
            """)
        elif prediction['soil_type'] == "Silty":
            st.warning("""
            **Additional Tips for Silty Soil:**
            - Avoid excessive compaction
            - Add organic matter for structure
            - Monitor drainage during heavy rains
            - Use cover crops to prevent erosion
            """)
        
        st.markdown("---")
        
        # Next steps
        st.markdown("### 🎯 Next Steps")
        
        next_col1, next_col2, next_col3 = st.columns(3)
        
        with next_col1:
            st.markdown("""
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px;">
                <h4>💧 Check Irrigation</h4>
                <p>Use the Smart Irrigation module to get water recommendations for this soil type.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with next_col2:
            st.markdown("""
            <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px;">
                <h4>🧪 Get Fertilizer Plan</h4>
                <p>Visit Fertilizer Advisory for NPK recommendations based on your soil.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with next_col3:
            st.markdown("""
            <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px;">
                <h4>📈 Estimate Yield</h4>
                <p>Check expected crop yield for this soil type in the Yield Estimator.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model info
        with st.expander("ℹ️ About This Detection"):
            st.markdown(f"""
            **Current Status:** Prototype Mode (Simulated Prediction)
            
            **How it works now:**
            - The system uses image file characteristics for simulation
            - File analyzed: {prediction['file_size_kb']} KB
            - This is a placeholder for demonstration purposes
            
            **Coming Soon:**
            - Real AI model (MobileNetV2) integration
            - Actual image analysis using deep learning
            - Higher accuracy with trained model
            - Additional soil parameters detection
            
            **Disclaimer:** This is currently a simulated prediction for demonstration. 
            For accurate soil testing, please consult agricultural testing labs.
            """)
    
    else:
        # Placeholder when no image uploaded
        st.info("👆 Please upload a soil image to begin analysis")
        
        # Sample images section
        st.markdown("### 📚 Sample Soil Types")
        
        sample_col1, sample_col2, sample_col3 = st.columns(3)
        
        with sample_col1:
            st.markdown("""
            <div style="background-color: #F4A460; padding: 30px; border-radius: 10px; text-align: center; color: white;">
                <h3>Sandy Soil</h3>
                <p>Light, grainy texture</p>
            </div>
            """, unsafe_allow_html=True)
        
        with sample_col2:
            st.markdown("""
            <div style="background-color: #8B4513; padding: 30px; border-radius: 10px; text-align: center; color: white;">
                <h3>Loamy Soil</h3>
                <p>Dark, crumbly texture</p>
            </div>
            """, unsafe_allow_html=True)
        
        with sample_col3:
            st.markdown("""
            <div style="background-color: #654321; padding: 30px; border-radius: 10px; text-align: center; color: white;">
                <h3>Clay Soil</h3>
                <p>Heavy, sticky texture</p>
            </div>
            """, unsafe_allow_html=True)
