"""
Utility functions for farm advisory system
"""

def get_crop_list():
    """Returns list of supported crops"""
    return [
        "Rice",
        "Wheat",
        "Cotton",
        "Sugarcane",
        "Maize",
        "Soybean",
        "Potato",
        "Tomato",
        "Onion",
        "Groundnut"
    ]

def get_soil_types():
    """Returns list of soil types"""
    return [
        "Clay",
        "Sandy",
        "Loamy",
        "Silty",
        "Peaty",
        "Chalky"
    ]

def get_growth_stages():
    """Returns growth stages for crops"""
    return [
        "Seedling/Germination",
        "Vegetative Growth",
        "Flowering",
        "Fruiting/Grain Filling",
        "Maturity/Harvest"
    ]

def get_soil_water_capacity(soil_type):
    """Returns water holding capacity for different soil types"""
    capacity_map = {
        "Clay": {"low": 25, "optimal_min": 30, "optimal_max": 60, "high": 70},
        "Sandy": {"low": 15, "optimal_min": 20, "optimal_max": 45, "high": 55},
        "Loamy": {"low": 20, "optimal_min": 25, "optimal_max": 55, "high": 65},
        "Silty": {"low": 22, "optimal_min": 27, "optimal_max": 57, "high": 67},
        "Peaty": {"low": 30, "optimal_min": 35, "optimal_max": 70, "high": 80},
        "Chalky": {"low": 18, "optimal_min": 23, "optimal_max": 50, "high": 60}
    }
    return capacity_map.get(soil_type, capacity_map["Loamy"])

def get_crop_water_requirement(crop_type):
    """Returns average water requirement in mm/day for different crops"""
    water_req = {
        "Rice": 7.5,
        "Wheat": 4.5,
        "Cotton": 6.0,
        "Sugarcane": 8.0,
        "Maize": 5.5,
        "Soybean": 5.0,
        "Potato": 4.0,
        "Tomato": 5.0,
        "Onion": 4.5,
        "Groundnut": 5.5
    }
    return water_req.get(crop_type, 5.0)

def format_npk(n, p, k):
    """Format NPK values"""
    return f"N: {n} kg/acre, P: {p} kg/acre, K: {k} kg/acre"


def explain_decision(inputs, result, decision_type="irrigation"):
    """
    Generate friendly explanation for farmers.
    Uses cautious, rule-based language without strong claims.
    
    Args:
        inputs: dict with input parameters
        result: dict with decision results
        decision_type: "irrigation", "fertilizer", or "yield"
    
    Returns:
        str: Farmer-friendly explanation
    """
    explanation_parts = []
    
    if decision_type == "irrigation":
        # Opening
        explanation_parts.append(
            f"📋 Based on current values for your {inputs.get('crop_type', 'crop')} "
            f"grown in {inputs.get('soil_type', 'soil')}, here is what the data suggests:"
        )
        
        # Moisture analysis
        moisture = inputs.get('moisture', 0)
        if moisture < 25:
            explanation_parts.append(
                f"⚠️ Your soil moisture is at {moisture}%. This is quite low. "
                f"It is safer to consider watering soon to avoid crop stress."
            )
        elif moisture < 40:
            explanation_parts.append(
                f"💡 Your soil moisture is at {moisture}%. You may consider watering "
                f"to maintain healthy crop growth."
            )
        elif moisture > 65:
            explanation_parts.append(
                f"✋ Your soil moisture is at {moisture}%. This appears high. "
                f"You may want to wait before adding more water."
            )
        else:
            explanation_parts.append(
                f"✅ Your soil moisture is at {moisture}%. This level seems reasonable "
                f"for now."
            )
        
        # Rain forecast
        rain = inputs.get('rain_forecast', 0)
        if rain > 40:
            explanation_parts.append(
                f"🌧️ Based on weather reports showing {rain}mm rain expected, "
                f"it would be safer to delay watering and let nature help."
            )
        elif rain > 20:
            explanation_parts.append(
                f"☁️ Some rain ({rain}mm) is expected soon. You may consider "
                f"reducing water amount if you decide to irrigate."
            )
        elif rain > 0:
            explanation_parts.append(
                f"🌤️ Light rain ({rain}mm) is in the forecast, but it may not be enough. "
                f"Please monitor your field conditions."
            )
        
        # Temperature note
        temp = inputs.get('temperature', 25)
        if temp > 35:
            explanation_parts.append(
                f"🌡️ Temperature is high at {temp}°C. Crops tend to need more water "
                f"in such heat. You may consider watering in early morning or evening."
            )
        elif temp < 15:
            explanation_parts.append(
                f"🌡️ Temperature is cool at {temp}°C. Crops generally need less water "
                f"in cooler weather."
            )
        
        # Final recommendation
        if result.get('needs_irrigation'):
            water_amount = result.get('water_amount_mm', 0)
            explanation_parts.append(
                f"💧 Based on these factors, applying around {water_amount}mm of water "
                f"appears reasonable. However, please also check your field personally "
                f"before making the final decision."
            )
        else:
            explanation_parts.append(
                f"⏸️ Based on these factors, you may consider waiting before watering. "
                f"Please monitor your field and adjust as needed."
            )
    
    elif decision_type == "fertilizer":
        # Opening
        explanation_parts.append(
            f"📋 Based on your {inputs.get('crop_type', 'crop')} in "
            f"{inputs.get('soil_type', 'soil')} soil at {inputs.get('growth_stage', 'current')} stage:"
        )
        
        # NPK explanation
        stage_npk = result.get('stage_npk', {})
        n_val = stage_npk.get('N', 0)
        p_val = stage_npk.get('P', 0)
        k_val = stage_npk.get('K', 0)
        
        explanation_parts.append(
            f"💡 You may consider applying approximately {n_val} kg Nitrogen, "
            f"{p_val} kg Phosphorus, and {k_val} kg Potassium per acre."
        )
        
        explanation_parts.append(
            f"🌱 Based on agricultural guidelines, crops at this stage generally "
            f"benefit from these nutrients. However, a soil test would give you "
            f"more accurate information about what your soil actually needs."
        )
        
        # Timing note
        explanation_parts.append(
            f"⏰ It is safer to split the application into smaller doses rather than "
            f"applying everything at once. This helps prevent nutrient loss and gives "
            f"better results."
        )
        
        # Organic option
        explanation_parts.append(
            f"🌿 If you prefer, organic options like compost or farmyard manure can "
            f"also be considered. They work slower but improve soil health over time."
        )
    
    elif decision_type == "yield":
        # Opening
        explanation_parts.append(
            f"📋 Based on water availability for your {inputs.get('crop_type', 'crop')}:"
        )
        
        # Yield range
        yield_min = result.get('yield_min', 0)
        yield_max = result.get('yield_max', 0)
        
        explanation_parts.append(
            f"📊 You may expect somewhere between {yield_min} to {yield_max} quintals per acre. "
            f"This is an estimate based on typical conditions - actual results can vary."
        )
        
        # Water status
        water_status = result.get('water_status', '')
        if 'deficit' in water_status.lower():
            explanation_parts.append(
                f"⚠️ Based on current rainfall and irrigation plans, crops might face "
                f"some water shortage. You may consider increasing irrigation if possible."
            )
        elif 'excess' in water_status.lower():
            explanation_parts.append(
                f"💧 There appears to be plenty of water available. It would be safer "
                f"to avoid over-watering, as too much water can also reduce yield."
            )
        else:
            explanation_parts.append(
                f"✅ Water availability seems reasonable based on current plans."
            )
        
        # Financial note
        profit = result.get('profit', 0)
        if profit > 0:
            explanation_parts.append(
                f"💰 Based on approximate market prices, this crop may give you a profit. "
                f"However, prices can change, so please check current market rates in your area."
            )
        else:
            explanation_parts.append(
                f"💰 Based on approximate costs, you may want to review your expenses. "
                f"Consider consulting with local agricultural experts for cost reduction tips."
            )
    
    # General disclaimer
    explanation_parts.append(
        f"\n⚠️ **Please Note**: These are suggestions based on general agricultural "
        f"principles and the data you provided. Your local conditions may be different. "
        f"It is always safer to also observe your field personally and consult with "
        f"experienced farmers or agricultural officers in your area before making important decisions."
    )
    
    return "\n\n".join(explanation_parts)
