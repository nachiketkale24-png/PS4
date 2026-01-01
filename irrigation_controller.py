"""
Irrigation Decision Controller
Deterministic rule-based irrigation recommendation engine

Author: Backend Engineering Team
Purpose: Make irrigation decisions based purely on mathematical rules, not AI
"""

import json
from typing import Dict, Any


class IrrigationController:
    """
    Deterministic irrigation decision controller.
    Same inputs always produce same outputs.
    """
    
    # Soil water holding capacity thresholds (percentage)
    SOIL_THRESHOLDS = {
        "clay": {
            "field_capacity": 45,      # Maximum water clay can hold
            "wilting_point": 25,        # Below this, crop starts wilting
            "optimal_min": 35,          # Minimum optimal moisture
            "optimal_max": 42,          # Maximum optimal moisture
            "saturation": 80            # Above this is waterlogged
        },
        "loam": {
            "field_capacity": 35,
            "wilting_point": 18,
            "optimal_min": 25,
            "optimal_max": 32,
            "saturation": 75
        },
        "sandy": {
            "field_capacity": 25,
            "wilting_point": 10,
            "optimal_min": 15,
            "optimal_max": 22,
            "saturation": 65
        }
    }
    
    # Crop water requirements (mm/day) at different stages
    CROP_WATER_REQUIREMENTS = {
        "rice": {"germination": 5, "vegetative": 7, "flowering": 9, "harvest": 3},
        "wheat": {"germination": 3, "vegetative": 5, "flowering": 6, "harvest": 2},
        "cotton": {"germination": 4, "vegetative": 6, "flowering": 8, "harvest": 3},
        "maize": {"germination": 3.5, "vegetative": 5.5, "flowering": 7, "harvest": 2.5},
        "sugarcane": {"germination": 6, "vegetative": 8, "flowering": 10, "harvest": 4},
        "soybean": {"germination": 3, "vegetative": 5, "flowering": 6.5, "harvest": 2},
        "potato": {"germination": 3, "vegetative": 4.5, "flowering": 5.5, "harvest": 2},
        "tomato": {"germination": 3.5, "vegetative": 5, "flowering": 6, "harvest": 2.5},
        "onion": {"germination": 3, "vegetative": 4.5, "flowering": 5, "harvest": 2},
        "groundnut": {"germination": 3.5, "vegetative": 5, "flowering": 6.5, "harvest": 2.5}
    }
    
    # Irrigation frequency based on soil type (days between irrigation)
    IRRIGATION_FREQUENCY = {
        "clay": 5,      # Clay retains water longer
        "loam": 3,      # Loam is balanced
        "sandy": 2      # Sandy drains quickly, needs frequent watering
    }
    
    # Irrigation methods based on soil and crop
    IRRIGATION_METHODS = {
        "default": "drip",
        "rice": "flood",
        "sugarcane": "furrow"
    }
    
    def calculate_irrigation_decision(
        self,
        soil_type: str,
        crop_name: str,
        current_soil_moisture: float,
        temperature: float,
        rainfall_probability: float,
        crop_stage: str
    ) -> Dict[str, Any]:
        """
        Calculate irrigation decision using deterministic rules.
        
        Args:
            soil_type: Type of soil (clay, loam, sandy)
            crop_name: Name of the crop
            current_soil_moisture: Current moisture level (0-100%)
            temperature: Temperature in Celsius
            rainfall_probability: Probability of rain (0-100%)
            crop_stage: Current crop stage (germination, vegetative, flowering, harvest)
        
        Returns:
            Dictionary containing irrigation decision and parameters
        """
        # Normalize inputs to lowercase
        soil_type = soil_type.lower()
        crop_name = crop_name.lower()
        crop_stage = crop_stage.lower()
        
        # Get soil thresholds (default to loam if unknown)
        soil_params = self.SOIL_THRESHOLDS.get(soil_type, self.SOIL_THRESHOLDS["loam"])
        
        # Get crop water requirement (default to wheat if unknown)
        crop_water = self.CROP_WATER_REQUIREMENTS.get(
            crop_name, 
            self.CROP_WATER_REQUIREMENTS["wheat"]
        )
        daily_water_need = crop_water.get(crop_stage, 5.0)
        
        # RULE 6: If moisture > 80%, no irrigation needed
        if current_soil_moisture > soil_params["saturation"]:
            return self._create_response(
                need_irrigation=False,
                water_required_mm=0,
                duration_minutes=0,
                frequency_days=0,
                method=self._get_irrigation_method(crop_name),
                risks=["Over-saturation risk", "Waterlogging", "Root rot possible"],
                explanation=f"Soil moisture is {current_soil_moisture}% which is too high. "
                           f"Do not irrigate. Allow soil to dry naturally to avoid waterlogging."
            )
        
        # RULE 7: High rainfall probability reduces irrigation need
        # If rainfall probability > 65%, minimize water
        rainfall_factor = self._calculate_rainfall_factor(rainfall_probability)
        
        # Calculate moisture deficit (how much water soil needs to reach optimal)
        moisture_deficit = max(0, soil_params["optimal_min"] - current_soil_moisture)
        
        # Temperature adjustment factor
        # Higher temperature increases evapotranspiration
        # Formula: For every degree above 25°C, add 2% to water need
        # For every degree below 25°C, reduce 2% from water need
        temp_factor = 1.0 + ((temperature - 25) * 0.02)
        temp_factor = max(0.7, min(1.3, temp_factor))  # Clamp between 0.7 and 1.3
        
        # RULE 5: Flowering stage gets slightly higher priority
        # Add 15% more water during flowering
        stage_factor = 1.15 if crop_stage == "flowering" else 1.0
        
        # Calculate base water requirement (mm)
        # Formula: (Daily need × temp adjustment × stage priority) + moisture deficit compensation
        base_water_mm = (daily_water_need * temp_factor * stage_factor) + (moisture_deficit * 0.5)
        
        # Apply rainfall reduction
        water_required_mm = base_water_mm * rainfall_factor
        
        # Determine if irrigation is needed
        # Irrigation needed if:
        # 1. Moisture below optimal AND
        # 2. Water required (after rainfall adjustment) > 0 AND
        # 3. Moisture not already saturated
        need_irrigation = (
            current_soil_moisture < soil_params["optimal_min"] and
            water_required_mm > 1.0 and  # At least 1mm needed
            current_soil_moisture <= soil_params["saturation"]
        )
        
        if not need_irrigation:
            water_required_mm = 0
        
        # Round water requirement to 1 decimal
        water_required_mm = round(water_required_mm, 1)
        
        # Calculate irrigation duration in minutes
        # Assumption: Average irrigation rate is 10mm/hour
        irrigation_rate_mm_per_hour = 10
        duration_minutes = round((water_required_mm / irrigation_rate_mm_per_hour) * 60, 0)
        
        # RULE 4: Sandy soil needs more frequent irrigation, clay needs less
        frequency_days = self.IRRIGATION_FREQUENCY.get(soil_type, 3)
        
        # Get irrigation method
        method = self._get_irrigation_method(crop_name)
        
        # Identify risks
        risks = self._identify_risks(
            current_soil_moisture,
            soil_params,
            temperature,
            rainfall_probability,
            crop_stage
        )
        
        # Generate farmer-friendly explanation
        explanation = self._generate_explanation(
            need_irrigation,
            current_soil_moisture,
            soil_params,
            water_required_mm,
            temperature,
            rainfall_probability,
            crop_stage,
            soil_type
        )
        
        return self._create_response(
            need_irrigation=need_irrigation,
            water_required_mm=water_required_mm,
            duration_minutes=int(duration_minutes),
            frequency_days=frequency_days,
            method=method,
            risks=risks,
            explanation=explanation
        )
    
    def _calculate_rainfall_factor(self, rainfall_probability: float) -> float:
        """
        Calculate water reduction factor based on rainfall probability.
        
        RULE 7: If rainfall_probability > 65%, minimize water
        
        Formula:
        - 0-20% rain: 100% water (factor = 1.0)
        - 20-40% rain: 80% water (factor = 0.8)
        - 40-65% rain: 50% water (factor = 0.5)
        - 65-80% rain: 20% water (factor = 0.2)
        - 80-100% rain: 0% water (factor = 0.0)
        
        Args:
            rainfall_probability: Probability of rain (0-100%)
        
        Returns:
            Float between 0.0 and 1.0 representing water reduction factor
        """
        if rainfall_probability >= 80:
            return 0.0
        elif rainfall_probability >= 65:
            return 0.2
        elif rainfall_probability >= 40:
            return 0.5
        elif rainfall_probability >= 20:
            return 0.8
        else:
            return 1.0
    
    def _get_irrigation_method(self, crop_name: str) -> str:
        """
        Determine optimal irrigation method for crop.
        
        Args:
            crop_name: Name of the crop
        
        Returns:
            Irrigation method name
        """
        return self.IRRIGATION_METHODS.get(crop_name, self.IRRIGATION_METHODS["default"])
    
    def _identify_risks(
        self,
        moisture: float,
        soil_params: dict,
        temperature: float,
        rainfall_prob: float,
        crop_stage: str
    ) -> list:
        """
        Identify potential risks based on current conditions.
        
        Args:
            moisture: Current soil moisture
            soil_params: Soil threshold parameters
            temperature: Current temperature
            rainfall_prob: Rainfall probability
            crop_stage: Current crop stage
        
        Returns:
            List of risk descriptions
        """
        risks = []
        
        # Moisture-based risks
        if moisture < soil_params["wilting_point"]:
            risks.append("Critical water stress - crop wilting risk")
        elif moisture < soil_params["optimal_min"]:
            risks.append("Below optimal moisture - yield reduction possible")
        
        if moisture > soil_params["optimal_max"]:
            risks.append("High moisture - fungal disease risk")
        
        # Temperature-based risks
        if temperature > 38:
            risks.append("Extreme heat - increased evaporation")
        elif temperature < 10:
            risks.append("Cold stress - reduced water uptake")
        
        # Rainfall risks
        if rainfall_prob > 70 and moisture > soil_params["optimal_min"]:
            risks.append("Rain expected with adequate moisture - skip irrigation")
        
        # Stage-specific risks
        if crop_stage == "flowering" and moisture < soil_params["optimal_min"]:
            risks.append("Critical flowering stage needs adequate water")
        
        if not risks:
            risks.append("No significant risks detected")
        
        return risks
    
    def _generate_explanation(
        self,
        need_irrigation: bool,
        moisture: float,
        soil_params: dict,
        water_mm: float,
        temp: float,
        rain_prob: float,
        stage: str,
        soil_type: str
    ) -> str:
        """
        Generate simple, farmer-friendly explanation without jargon.
        
        Args:
            need_irrigation: Whether irrigation is needed
            moisture: Current moisture level
            soil_params: Soil parameters
            water_mm: Water required in mm
            temp: Temperature
            rain_prob: Rainfall probability
            stage: Crop stage
            soil_type: Type of soil
        
        Returns:
            Plain language explanation
        """
        if not need_irrigation:
            if moisture > soil_params["optimal_max"]:
                return (
                    f"Your soil has enough water ({moisture}%). "
                    f"No need to water now. Wait for soil to dry a bit."
                )
            elif rain_prob > 65:
                return (
                    f"Rain is likely ({rain_prob}% chance). "
                    f"Better to wait and let rain water your crop."
                )
            else:
                return (
                    f"Soil moisture is okay at {moisture}%. "
                    f"No watering needed right now."
                )
        else:
            explanation_parts = [
                f"Your {soil_type} soil currently has {moisture}% moisture."
            ]
            
            if moisture < soil_params["wilting_point"]:
                explanation_parts.append(
                    f"This is very low. Plants may start wilting soon."
                )
            else:
                explanation_parts.append(
                    f"This is below the ideal level for your crop."
                )
            
            if stage == "flowering":
                explanation_parts.append(
                    f"Your crop is flowering now and needs good water supply."
                )
            
            explanation_parts.append(
                f"Apply about {water_mm}mm of water."
            )
            
            if temp > 32:
                explanation_parts.append(
                    f"It's hot ({temp}°C), so water in the morning or evening."
                )
            
            if rain_prob > 20:
                explanation_parts.append(
                    f"Some rain may come ({rain_prob}% chance), so we reduced the water amount."
                )
            
            return " ".join(explanation_parts)
    
    def _create_response(
        self,
        need_irrigation: bool,
        water_required_mm: float,
        duration_minutes: int,
        frequency_days: int,
        method: str,
        risks: list,
        explanation: str
    ) -> Dict[str, Any]:
        """
        Create standardized JSON response.
        
        Args:
            need_irrigation: Boolean irrigation decision
            water_required_mm: Water amount in millimeters
            duration_minutes: Irrigation duration
            frequency_days: Days between irrigation
            method: Irrigation method
            risks: List of risk factors
            explanation: Farmer-friendly explanation
        
        Returns:
            Dictionary in JSON-serializable format
        """
        return {
            "need_irrigation": need_irrigation,
            "water_required_mm": water_required_mm,
            "recommended_duration_minutes": duration_minutes,
            "frequency_days": frequency_days,
            "irrigation_method": method,
            "risks": risks,
            "explanation": explanation
        }


# Convenience function for direct use
def get_irrigation_decision(
    soil_type: str,
    crop_name: str,
    current_soil_moisture: float,
    temperature: float,
    rainfall_probability: float,
    crop_stage: str
) -> str:
    """
    Get irrigation decision as JSON string.
    
    Args:
        soil_type: Type of soil (clay, loam, sandy)
        crop_name: Name of the crop
        current_soil_moisture: Current moisture level (0-100%)
        temperature: Temperature in Celsius
        rainfall_probability: Probability of rain (0-100%)
        crop_stage: Current crop stage (germination, vegetative, flowering, harvest)
    
    Returns:
        JSON string with irrigation decision
    """
    controller = IrrigationController()
    result = controller.calculate_irrigation_decision(
        soil_type=soil_type,
        crop_name=crop_name,
        current_soil_moisture=current_soil_moisture,
        temperature=temperature,
        rainfall_probability=rainfall_probability,
        crop_stage=crop_stage
    )
    return json.dumps(result, indent=2)


# Example usage
if __name__ == "__main__":
    # Example 1: Dry sandy soil with wheat in flowering stage
    print("Example 1: Sandy soil, low moisture, flowering stage")
    print(get_irrigation_decision(
        soil_type="sandy",
        crop_name="wheat",
        current_soil_moisture=12,
        temperature=28,
        rainfall_probability=15,
        crop_stage="flowering"
    ))
    print("\n" + "="*80 + "\n")
    
    # Example 2: Clay soil with good moisture and high rain probability
    print("Example 2: Clay soil, adequate moisture, rain expected")
    print(get_irrigation_decision(
        soil_type="clay",
        crop_name="rice",
        current_soil_moisture=38,
        temperature=30,
        rainfall_probability=75,
        crop_stage="vegetative"
    ))
    print("\n" + "="*80 + "\n")
    
    # Example 3: Over-saturated loam soil
    print("Example 3: Loam soil, over-saturated")
    print(get_irrigation_decision(
        soil_type="loam",
        crop_name="maize",
        current_soil_moisture=82,
        temperature=25,
        rainfall_probability=30,
        crop_stage="vegetative"
    ))
