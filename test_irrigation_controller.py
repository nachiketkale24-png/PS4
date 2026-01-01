"""
Unit Tests for Irrigation Controller
Tests all deterministic rules and edge cases
"""

import unittest
import json
from irrigation_controller import IrrigationController


class TestIrrigationController(unittest.TestCase):
    """Test suite for irrigation decision controller"""
    
    def setUp(self):
        """Set up test controller instance"""
        self.controller = IrrigationController()
    
    def test_deterministic_behavior(self):
        """
        Test RULE 1: Same inputs should always produce same outputs
        """
        # Run same calculation twice
        result1 = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        result2 = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Results must be identical
        self.assertEqual(result1, result2)
        self.assertEqual(result1["water_required_mm"], result2["water_required_mm"])
    
    def test_over_saturation_rule(self):
        """
        Test RULE 6: If moisture > 80%, irrigation should be False
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="clay",
            crop_name="rice",
            current_soil_moisture=85,
            temperature=28,
            rainfall_probability=20,
            crop_stage="vegetative"
        )
        
        self.assertFalse(result["need_irrigation"])
        self.assertEqual(result["water_required_mm"], 0)
        self.assertIn("waterlogging", result["explanation"].lower())
    
    def test_high_rainfall_probability(self):
        """
        Test RULE 7: If rainfall_probability > 65%, minimize water
        """
        # High rain probability should give minimal or no water
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=22,
            temperature=25,
            rainfall_probability=75,
            crop_stage="vegetative"
        )
        
        # Water should be minimal (20% of normal or 0)
        self.assertTrue(result["water_required_mm"] <= 2.0 or not result["need_irrigation"])
    
    def test_sandy_soil_frequent_irrigation(self):
        """
        Test RULE 4: Sandy soil needs more frequent irrigation
        """
        result_sandy = self.controller.calculate_irrigation_decision(
            soil_type="sandy",
            crop_name="wheat",
            current_soil_moisture=15,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        result_clay = self.controller.calculate_irrigation_decision(
            soil_type="clay",
            crop_name="wheat",
            current_soil_moisture=30,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Sandy soil should have higher frequency (lower days between irrigation)
        self.assertLess(
            result_sandy["frequency_days"],
            result_clay["frequency_days"]
        )
        self.assertEqual(result_sandy["frequency_days"], 2)
        self.assertEqual(result_clay["frequency_days"], 5)
    
    def test_flowering_stage_priority(self):
        """
        Test RULE 5: Flowering stage gets slightly higher water priority
        """
        result_flowering = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="flowering"
        )
        
        result_vegetative = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Flowering should require more water than vegetative stage
        self.assertGreater(
            result_flowering["water_required_mm"],
            result_vegetative["water_required_mm"]
        )
    
    def test_temperature_adjustment(self):
        """
        Test temperature factor: Higher temp increases water need
        """
        result_hot = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=35,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        result_cool = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=18,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Hot weather should require more water
        self.assertGreater(
            result_hot["water_required_mm"],
            result_cool["water_required_mm"]
        )
    
    def test_rainfall_factor_calculation(self):
        """
        Test rainfall factor calculation thresholds
        """
        # 0-20% rain: factor = 1.0
        self.assertEqual(self.controller._calculate_rainfall_factor(10), 1.0)
        
        # 20-40% rain: factor = 0.8
        self.assertEqual(self.controller._calculate_rainfall_factor(30), 0.8)
        
        # 40-65% rain: factor = 0.5
        self.assertEqual(self.controller._calculate_rainfall_factor(50), 0.5)
        
        # 65-80% rain: factor = 0.2
        self.assertEqual(self.controller._calculate_rainfall_factor(70), 0.2)
        
        # 80-100% rain: factor = 0.0
        self.assertEqual(self.controller._calculate_rainfall_factor(85), 0.0)
    
    def test_critical_wilting_point(self):
        """
        Test that very low moisture triggers critical risk
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=15,  # Below wilting point (18%)
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        self.assertTrue(result["need_irrigation"])
        self.assertIn("wilting", " ".join(result["risks"]).lower())
    
    def test_irrigation_method_selection(self):
        """
        Test correct irrigation method selection for different crops
        """
        # Rice should use flood irrigation
        result_rice = self.controller.calculate_irrigation_decision(
            soil_type="clay",
            crop_name="rice",
            current_soil_moisture=30,
            temperature=28,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        self.assertEqual(result_rice["irrigation_method"], "flood")
        
        # Wheat should use drip (default)
        result_wheat = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        self.assertEqual(result_wheat["irrigation_method"], "drip")
    
    def test_duration_calculation(self):
        """
        Test that duration is correctly calculated from water amount
        Assumption: 10mm/hour irrigation rate
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        if result["need_irrigation"]:
            # Duration (minutes) should be (water_mm / 10) * 60
            expected_duration = (result["water_required_mm"] / 10) * 60
            self.assertAlmostEqual(
                result["recommended_duration_minutes"],
                expected_duration,
                delta=1  # Allow 1 minute rounding difference
            )
    
    def test_no_irrigation_adequate_moisture(self):
        """
        Test that no irrigation is recommended when moisture is adequate
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=28,  # Within optimal range (25-32)
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        self.assertFalse(result["need_irrigation"])
        self.assertEqual(result["water_required_mm"], 0)
    
    def test_json_serializable_output(self):
        """
        Test that output can be serialized to JSON
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Should not raise exception
        try:
            json_str = json.dumps(result)
            parsed = json.loads(json_str)
            self.assertEqual(result, parsed)
        except Exception as e:
            self.fail(f"JSON serialization failed: {e}")
    
    def test_case_insensitive_inputs(self):
        """
        Test that inputs are normalized (case insensitive)
        """
        result1 = self.controller.calculate_irrigation_decision(
            soil_type="CLAY",
            crop_name="WHEAT",
            current_soil_moisture=30,
            temperature=25,
            rainfall_probability=10,
            crop_stage="FLOWERING"
        )
        
        result2 = self.controller.calculate_irrigation_decision(
            soil_type="clay",
            crop_name="wheat",
            current_soil_moisture=30,
            temperature=25,
            rainfall_probability=10,
            crop_stage="flowering"
        )
        
        self.assertEqual(result1, result2)
    
    def test_unknown_crop_defaults(self):
        """
        Test that unknown crops default to reasonable values
        """
        result = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="unknown_crop_xyz",
            current_soil_moisture=20,
            temperature=25,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        
        # Should not crash, should return valid result
        self.assertIsInstance(result["need_irrigation"], bool)
        self.assertIsInstance(result["water_required_mm"], (int, float))
    
    def test_extreme_temperature_risks(self):
        """
        Test that extreme temperatures are flagged as risks
        """
        # Extreme heat
        result_hot = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=25,
            temperature=42,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        risks_text = " ".join(result_hot["risks"]).lower()
        self.assertIn("heat", risks_text)
        
        # Extreme cold
        result_cold = self.controller.calculate_irrigation_decision(
            soil_type="loam",
            crop_name="wheat",
            current_soil_moisture=25,
            temperature=5,
            rainfall_probability=10,
            crop_stage="vegetative"
        )
        risks_text = " ".join(result_cold["risks"]).lower()
        self.assertIn("cold", risks_text)


# Run tests
if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
