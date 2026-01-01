"""
Fertilizer Recommendation Module
Rule-based fertilizer recommendation system
"""

import streamlit as st
from utils import get_crop_list, get_soil_types, get_growth_stages, format_npk

def get_npk_recommendation(crop_type, soil_type, growth_stage):
    """
    Calculate NPK requirements based on crop, soil, and growth stage
    
    Returns: dict with NPK values, timing, and organic alternatives
    """
    
    # Base NPK requirements for different crops (kg/acre)
    crop_npk_base = {
        "Rice": {"N": 120, "P": 60, "K": 40},
        "Wheat": {"N": 100, "P": 50, "K": 30},
        "Cotton": {"N": 80, "P": 40, "K": 40},
        "Sugarcane": {"N": 200, "P": 80, "K": 80},
        "Maize": {"N": 90, "P": 45, "K": 35},
        "Soybean": {"N": 30, "P": 60, "K": 40},
        "Potato": {"N": 100, "P": 80, "K": 100},
        "Tomato": {"N": 100, "P": 50, "K": 50},
        "Onion": {"N": 80, "P": 40, "K": 40},
        "Groundnut": {"N": 25, "P": 50, "K": 75}
    }
    
    # Soil type adjustments (multiplier)
    soil_adjustments = {
        "Clay": {"N": 0.9, "P": 1.1, "K": 1.0},
        "Sandy": {"N": 1.2, "P": 0.9, "K": 1.2},
        "Loamy": {"N": 1.0, "P": 1.0, "K": 1.0},
        "Silty": {"N": 0.95, "P": 1.05, "K": 1.0},
        "Peaty": {"N": 0.8, "P": 1.2, "K": 1.1},
        "Chalky": {"N": 1.1, "P": 1.3, "K": 1.0}
    }
    
    # Growth stage distribution (percentage of total)
    stage_distribution = {
        "Seedling/Germination": {"N": 0.20, "P": 0.40, "K": 0.20},
        "Vegetative Growth": {"N": 0.40, "P": 0.30, "K": 0.30},
        "Flowering": {"N": 0.25, "P": 0.20, "K": 0.30},
        "Fruiting/Grain Filling": {"N": 0.10, "P": 0.10, "K": 0.15},
        "Maturity/Harvest": {"N": 0.05, "P": 0.00, "K": 0.05}
    }
    
    # Get base NPK for crop
    base_npk = crop_npk_base.get(crop_type, {"N": 80, "P": 40, "K": 40})
    
    # Apply soil adjustments
    soil_adj = soil_adjustments.get(soil_type, {"N": 1.0, "P": 1.0, "K": 1.0})
    total_n = round(base_npk["N"] * soil_adj["N"])
    total_p = round(base_npk["P"] * soil_adj["P"])
    total_k = round(base_npk["K"] * soil_adj["K"])
    
    # Get stage-specific application
    stage_dist = stage_distribution.get(growth_stage, {"N": 0.25, "P": 0.25, "K": 0.25})
    stage_n = round(total_n * stage_dist["N"])
    stage_p = round(total_p * stage_dist["P"])
    stage_k = round(total_k * stage_dist["K"])
    
    # Generate split application timing
    timing = generate_application_timing(growth_stage)
    
    # Generate organic alternatives
    organic_alt = generate_organic_alternatives(stage_n, stage_p, stage_k)
    
    # Generate explanation
    explanation = generate_fertilizer_explanation(
        crop_type, soil_type, growth_stage, 
        total_n, total_p, total_k,
        stage_n, stage_p, stage_k,
        soil_adj
    )
    
    return {
        "total_npk": {"N": total_n, "P": total_p, "K": total_k},
        "stage_npk": {"N": stage_n, "P": stage_p, "K": stage_k},
        "timing": timing,
        "organic_alternatives": organic_alt,
        "explanation": explanation
    }

def generate_application_timing(growth_stage):
    """Generate split application timing recommendations"""
    timing_map = {
        "Seedling/Germination": [
            "Apply at sowing/transplanting",
            "Apply 50% of recommended dose as basal",
            "Apply remaining 50% after 2 weeks"
        ],
        "Vegetative Growth": [
            "Apply in 2 equal splits",
            "First dose immediately",
            "Second dose after 15-20 days"
        ],
        "Flowering": [
            "Apply in single dose at flower initiation",
            "Focus on potassium for flower/fruit development",
            "Reduce nitrogen to prevent excessive vegetative growth"
        ],
        "Fruiting/Grain Filling": [
            "Apply light dose to support fruit development",
            "Focus on potassium (K)",
            "Minimal nitrogen to avoid延delaying maturity"
        ],
        "Maturity/Harvest": [
            "Minimal to no fertilizer needed",
            "Stop nitrogen application completely",
            "Allow crop to mature naturally"
        ]
    }
    return timing_map.get(growth_stage, ["Apply as recommended by local agricultural expert"])

def generate_organic_alternatives(n, p, k):
    """Generate organic fertilizer alternatives"""
    alternatives = []
    
    # Nitrogen sources
    if n > 0:
        compost_kg = round(n * 15)  # ~7% N in good compost
        alternatives.append(f"**For Nitrogen**: {compost_kg} kg/acre of well-decomposed compost or farmyard manure")
        alternatives.append(f"   OR {round(n * 5)} kg/acre of neem cake")
    
    # Phosphorus sources
    if p > 0:
        bone_meal_kg = round(p * 6)  # ~15% P in bone meal
        alternatives.append(f"**For Phosphorus**: {bone_meal_kg} kg/acre of bone meal")
        alternatives.append(f"   OR {round(p * 4)} kg/acre of rock phosphate")
    
    # Potassium sources
    if k > 0:
        wood_ash_kg = round(k * 15)  # ~5-7% K in wood ash
        alternatives.append(f"**For Potassium**: {wood_ash_kg} kg/acre of wood ash")
        alternatives.append(f"   OR Apply kelp meal or greensand as per availability")
    
    return alternatives

def generate_fertilizer_explanation(crop, soil, stage, total_n, total_p, total_k, 
                                    stage_n, stage_p, stage_k, soil_adj):
    """Generate detailed explanation of fertilizer recommendation"""
    
    explanation_parts = []
    
    # Crop requirement
    explanation_parts.append(f"**🌾 Crop Requirement**: {crop} has specific nutrient needs throughout its growth cycle. "
                            f"The total seasonal requirement is approximately {total_n}-{total_p}-{total_k} (N-P-K) kg/acre.")
    
    # Soil type impact
    soil_impact = []
    if soil_adj["N"] > 1.0:
        soil_impact.append(f"nitrogen increased due to {soil} soil's low retention")
    elif soil_adj["N"] < 1.0:
        soil_impact.append(f"nitrogen reduced as {soil} soil retains it well")
    
    if soil_adj["P"] > 1.0:
        soil_impact.append(f"phosphorus increased as {soil} soil tends to fix P")
    elif soil_adj["P"] < 1.0:
        soil_impact.append(f"phosphorus reduced due to better availability in {soil} soil")
    
    if soil_impact:
        explanation_parts.append(f"**🏞️ Soil Adjustment**: The recommendation is adjusted because {', and '.join(soil_impact)}.")
    
    # Growth stage
    explanation_parts.append(f"**🌱 Growth Stage**: Currently in {stage} stage. "
                            f"At this stage, the crop needs {stage_n}-{stage_p}-{stage_k} (N-P-K) kg/acre.")
    
    # Nutrient roles
    nutrient_roles = []
    if stage_n > 0:
        nutrient_roles.append("**Nitrogen (N)** promotes leaf and stem growth")
    if stage_p > 0:
        nutrient_roles.append("**Phosphorus (P)** supports root development and energy transfer")
    if stage_k > 0:
        nutrient_roles.append("**Potassium (K)** enhances disease resistance and fruit quality")
    
    if nutrient_roles:
        explanation_parts.append("**💡 Why These Nutrients**: " + ", ".join(nutrient_roles) + ".")
    
    # Deterministic note
    explanation_parts.append("**📐 Calculation Method**: This recommendation is based on established agricultural "
                            "science and soil chemistry principles, not AI guessing. The values are calculated "
                            "using crop-specific requirements, soil characteristics, and growth stage needs.")
    
    return "\n\n".join(explanation_parts)


def show_fertilizer_module():
    """Display the Fertilizer Recommendation Module UI"""
    st.header("🧪 Fertilizer Recommendation")
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Crop Information")
        crop_type = st.selectbox("Select Crop", get_crop_list(), key="fert_crop")
        soil_type = st.selectbox("Soil Type", get_soil_types(), key="fert_soil")
    
    with col2:
        st.subheader("🌱 Growth Stage")
        growth_stage = st.selectbox("Current Growth Stage", get_growth_stages(), key="fert_stage")
    
    st.markdown("---")
    
    # Analyze button
    if st.button("🔬 Get Fertilizer Recommendation", type="primary", use_container_width=True):
        result = get_npk_recommendation(crop_type, soil_type, growth_stage)
        
        st.markdown("### 📊 Fertilizer Recommendation")
        
        # Display total and stage-specific NPK
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.info("#### 📦 Total Seasonal Requirement")
            st.markdown(f"**N-P-K**: {result['total_npk']['N']}-{result['total_npk']['P']}-{result['total_npk']['K']} kg/acre")
            st.metric("Nitrogen (N)", f"{result['total_npk']['N']} kg/acre")
            st.metric("Phosphorus (P)", f"{result['total_npk']['P']} kg/acre")
            st.metric("Potassium (K)", f"{result['total_npk']['K']} kg/acre")
        
        with metric_col2:
            st.success(f"#### 🎯 Current Stage: {growth_stage}")
            st.markdown(f"**N-P-K**: {result['stage_npk']['N']}-{result['stage_npk']['P']}-{result['stage_npk']['K']} kg/acre")
            st.metric("Nitrogen (N)", f"{result['stage_npk']['N']} kg/acre")
            st.metric("Phosphorus (P)", f"{result['stage_npk']['P']} kg/acre")
            st.metric("Potassium (K)", f"{result['stage_npk']['K']} kg/acre")
        
        st.markdown("---")
        
        # Application timing
        st.markdown("### ⏰ Split Application Timing")
        with st.expander("View Application Schedule", expanded=True):
            for i, timing in enumerate(result['timing'], 1):
                st.markdown(f"{i}. {timing}")
        
        # Organic alternatives
        st.markdown("### 🌿 Organic Alternatives")
        with st.expander("View Organic Options", expanded=False):
            st.markdown("Consider these organic alternatives for sustainable farming:")
            for alt in result['organic_alternatives']:
                st.markdown(f"- {alt}")
        
        # Detailed explanation
        st.markdown("### 📝 Detailed Explanation")
        with st.expander("Why These Recommendations?", expanded=True):
            st.markdown(result['explanation'])
