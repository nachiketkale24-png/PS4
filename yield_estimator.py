"""
Yield Estimator Module
Estimate crop yield based on various factors
"""

import streamlit as st
from utils import get_crop_list

def estimate_yield(crop_type, rainfall_mm, irrigation_level):
    """
    Estimate crop yield based on water availability and management
    
    Returns: dict with yield range, cost-benefit analysis
    """
    
    # Base yield potential (quintals/acre) under optimal conditions
    base_yields = {
        "Rice": 25,
        "Wheat": 20,
        "Cotton": 8,  # quintals of cotton lint
        "Sugarcane": 300,
        "Maize": 22,
        "Soybean": 12,
        "Potato": 80,
        "Tomato": 120,
        "Onion": 100,
        "Groundnut": 10
    }
    
    # Water requirement categories (total mm needed for season)
    water_requirements = {
        "Rice": 1200,
        "Wheat": 450,
        "Cotton": 700,
        "Sugarcane": 2000,
        "Maize": 600,
        "Soybean": 500,
        "Potato": 500,
        "Tomato": 600,
        "Onion": 450,
        "Groundnut": 550
    }
    
    # Get base values
    base_yield = base_yields.get(crop_type, 15)
    water_needed = water_requirements.get(crop_type, 600)
    
    # Calculate total water availability
    # Irrigation level: Low (30%), Medium (50%), High (70%) of requirement
    irrigation_percentages = {
        "Low (minimal irrigation)": 0.30,
        "Medium (regular irrigation)": 0.50,
        "High (intensive irrigation)": 0.70
    }
    
    irrigation_contribution = water_needed * irrigation_percentages.get(irrigation_level, 0.50)
    total_water = rainfall_mm + irrigation_contribution
    
    # Calculate water fulfillment ratio
    water_fulfillment = min(total_water / water_needed, 1.2)  # Cap at 120%
    
    # Determine yield multiplier based on water fulfillment
    if water_fulfillment < 0.5:
        yield_multiplier = 0.3  # Severe water stress
        water_status = "Severe water deficit"
    elif water_fulfillment < 0.7:
        yield_multiplier = 0.5  # Moderate water stress
        water_status = "Moderate water deficit"
    elif water_fulfillment < 0.85:
        yield_multiplier = 0.75  # Mild water stress
        water_status = "Mild water deficit"
    elif water_fulfillment <= 1.1:
        yield_multiplier = 1.0  # Optimal
        water_status = "Optimal water availability"
    else:
        yield_multiplier = 0.85  # Excess water can reduce yield
        water_status = "Excess water (potential waterlogging)"
    
    # Calculate expected yield range
    expected_yield = base_yield * yield_multiplier
    yield_min = round(expected_yield * 0.85, 1)  # -15% variation
    yield_max = round(expected_yield * 1.15, 1)  # +15% variation
    
    # Cost-benefit analysis (simplified dummy values)
    cost_per_acre = calculate_cost(crop_type, irrigation_level)
    revenue = calculate_revenue(crop_type, expected_yield)
    profit = revenue - cost_per_acre
    roi = round((profit / cost_per_acre) * 100, 1) if cost_per_acre > 0 else 0
    
    # Generate explanation
    explanation = generate_yield_explanation(
        crop_type, rainfall_mm, irrigation_level, water_needed,
        total_water, water_fulfillment, water_status,
        yield_multiplier, base_yield
    )
    
    return {
        "yield_min": yield_min,
        "yield_max": yield_max,
        "expected_yield": round(expected_yield, 1),
        "water_status": water_status,
        "water_fulfillment": round(water_fulfillment * 100, 1),
        "cost": cost_per_acre,
        "revenue": revenue,
        "profit": profit,
        "roi": roi,
        "explanation": explanation
    }

def calculate_cost(crop_type, irrigation_level):
    """Calculate approximate cost per acre (dummy values in INR)"""
    
    # Base costs (seeds, labor, basic inputs)
    base_costs = {
        "Rice": 15000,
        "Wheat": 12000,
        "Cotton": 18000,
        "Sugarcane": 35000,
        "Maize": 13000,
        "Soybean": 11000,
        "Potato": 25000,
        "Tomato": 30000,
        "Onion": 22000,
        "Groundnut": 14000
    }
    
    # Irrigation costs
    irrigation_costs = {
        "Low (minimal irrigation)": 2000,
        "Medium (regular irrigation)": 5000,
        "High (intensive irrigation)": 8000
    }
    
    base = base_costs.get(crop_type, 15000)
    irr_cost = irrigation_costs.get(irrigation_level, 5000)
    
    return base + irr_cost

def calculate_revenue(crop_type, yield_quintals):
    """Calculate approximate revenue (dummy values in INR)"""
    
    # Market prices per quintal (approximate)
    market_prices = {
        "Rice": 2000,
        "Wheat": 2100,
        "Cotton": 6000,
        "Sugarcane": 300,
        "Maize": 1800,
        "Soybean": 4000,
        "Potato": 800,
        "Tomato": 1200,
        "Onion": 1500,
        "Groundnut": 5500
    }
    
    price = market_prices.get(crop_type, 2000)
    return round(yield_quintals * price)

def generate_yield_explanation(crop_type, rainfall, irrigation_level, water_needed,
                               total_water, fulfillment, water_status, yield_mult, base_yield):
    """Generate detailed explanation of yield estimation"""
    
    explanation_parts = []
    
    # Water requirement
    explanation_parts.append(
        f"**💧 Water Requirement**: {crop_type} needs approximately {water_needed}mm of water "
        f"throughout the growing season for optimal yield."
    )
    
    # Water sources
    explanation_parts.append(
        f"**🌧️ Water Sources**: Expected rainfall of {rainfall}mm plus {irrigation_level} "
        f"contributes a total of approximately {round(total_water)}mm of water."
    )
    
    # Water fulfillment
    fulfillment_pct = round(fulfillment * 100, 1)
    explanation_parts.append(
        f"**📊 Water Fulfillment**: The crop will receive {fulfillment_pct}% of its water requirement. "
        f"Status: {water_status}."
    )
    
    # Yield impact
    if yield_mult >= 1.0:
        explanation_parts.append(
            f"**✅ Yield Impact**: Water availability is optimal. Expected to achieve "
            f"{round(yield_mult * 100)}% of the maximum potential yield ({base_yield} quintals/acre)."
        )
    elif yield_mult >= 0.75:
        explanation_parts.append(
            f"**⚠️ Yield Impact**: Mild water stress will reduce yield to approximately "
            f"{round(yield_mult * 100)}% of maximum potential ({base_yield} quintals/acre). "
            f"Consider increasing irrigation if possible."
        )
    else:
        explanation_parts.append(
            f"**🔴 Yield Impact**: Significant water stress will reduce yield to approximately "
            f"{round(yield_mult * 100)}% of maximum potential ({base_yield} quintals/acre). "
            f"Improved irrigation is strongly recommended."
        )
    
    # Deterministic note
    explanation_parts.append(
        "**📐 Calculation Method**: This estimate is based on established crop-water relationships "
        "and agricultural research data. The yield multiplier is calculated deterministically based on "
        "the water stress index. This is not an AI prediction but a mathematical relationship between "
        "water availability and crop productivity."
    )
    
    return "\n\n".join(explanation_parts)


def show_yield_estimator():
    """Display the Yield Estimator Module UI"""
    st.header("📈 Crop Yield Estimator")
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Crop Selection")
        crop_type = st.selectbox("Select Crop", get_crop_list(), key="yield_crop")
    
    with col2:
        st.subheader("💧 Water Management")
        irrigation_level = st.selectbox(
            "Irrigation Level",
            ["Low (minimal irrigation)", "Medium (regular irrigation)", "High (intensive irrigation)"],
            index=1,
            key="yield_irrigation"
        )
    
    st.subheader("🌦️ Seasonal Rainfall")
    rainfall_mm = st.slider(
        "Expected Total Rainfall (mm) for growing season",
        0, 1500, 400,
        step=50,
        key="yield_rainfall"
    )
    
    st.markdown("---")
    
    # Estimate button
    if st.button("📊 Estimate Yield", type="primary", use_container_width=True):
        result = estimate_yield(crop_type, rainfall_mm, irrigation_level)
        
        st.markdown("### 🎯 Yield Estimation Results")
        
        # Yield prediction
        st.success(f"### Expected Yield: {result['yield_min']} - {result['yield_max']} quintals/acre")
        st.info(f"**Most Likely**: {result['expected_yield']} quintals/acre")
        
        # Water status
        water_col1, water_col2 = st.columns(2)
        with water_col1:
            st.metric(
                "💧 Water Fulfillment",
                f"{result['water_fulfillment']}%",
                delta=result['water_status']
            )
        with water_col2:
            st.metric(
                "🌱 Yield Status",
                f"{result['expected_yield']} q/acre",
                delta=f"Range: {result['yield_min']}-{result['yield_max']}"
            )
        
        st.markdown("---")
        
        # Cost-Benefit Analysis
        st.markdown("### 💰 Cost vs Benefit Analysis")
        
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        
        with fin_col1:
            st.metric("📤 Total Cost", f"₹{result['cost']:,}")
        
        with fin_col2:
            st.metric("📥 Expected Revenue", f"₹{result['revenue']:,}")
        
        with fin_col3:
            profit_delta = "Profitable" if result['profit'] > 0 else "Loss"
            st.metric("💵 Profit", f"₹{result['profit']:,}", delta=profit_delta)
        
        with fin_col4:
            st.metric("📊 ROI", f"{result['roi']}%")
        
        # Cost breakdown note
        with st.expander("💡 About Cost Estimation"):
            st.markdown("""
            **Note**: The cost and revenue figures are placeholder estimates based on typical values:
            - Costs include: seeds, labor, fertilizers, pesticides, and irrigation
            - Revenue based on: average market prices (subject to market fluctuations)
            - Actual costs and revenues vary by region, season, and market conditions
            
            **This is for demonstration purposes only.** Consult local agricultural experts for precise financial planning.
            """)
        
        st.markdown("---")
        
        # Detailed explanation
        st.markdown("### 📝 How This Was Calculated")
        with st.expander("View Detailed Explanation", expanded=True):
            st.markdown(result['explanation'])
