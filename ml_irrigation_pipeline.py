"""
Soil Nutrient + Irrigation ML Pipeline
Predicts irrigation need and provides fertilizer recommendations

Author: ML Engineering Team
Purpose: Train and evaluate models for irrigation decision support
Note: Beginner-friendly code with extensive comments
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================================
# STEP 1: GENERATE SAMPLE DATASET
# ============================================================================

def generate_sample_dataset(n_samples=1000):
    """
    Generate synthetic training data for irrigation prediction.
    In production, this would be replaced with real field data.
    
    Args:
        n_samples: Number of samples to generate
    
    Returns:
        DataFrame with soil, nutrient, and irrigation data
    """
    print(f"📊 Generating {n_samples} sample records...")
    
    np.random.seed(42)  # For reproducibility - same random numbers every time
    
    # Define possible categories
    soil_types = ['clay', 'loam', 'sandy']
    crop_stages = ['germination', 'vegetative', 'flowering', 'harvest']
    
    data = {
        # Categorical features
        'soil_type': np.random.choice(soil_types, n_samples),
        'crop_stage': np.random.choice(crop_stages, n_samples),
        
        # Nutrient levels (in ppm or kg/acre)
        'nitrogen': np.random.uniform(20, 200, n_samples),      # N content
        'phosphorus': np.random.uniform(10, 100, n_samples),    # P content
        'potassium': np.random.uniform(10, 150, n_samples),     # K content
        
        # Soil properties
        'ph': np.random.uniform(5.0, 8.5, n_samples),           # Soil pH
        'moisture': np.random.uniform(10, 90, n_samples),       # Moisture %
        
        # Environmental conditions
        'temperature': np.random.uniform(15, 40, n_samples),    # Temperature °C
        'rainfall_prob': np.random.uniform(0, 100, n_samples),  # Rain probability %
    }
    
    df = pd.DataFrame(data)
    
    # Generate target variable using logical rules
    # This simulates real-world irrigation decisions
    irrigation_required = []
    
    for idx, row in df.iterrows():
        # Rule-based target generation (similar to our deterministic controller)
        need_irrigation = 0  # Default: no irrigation
        
        # Low moisture triggers irrigation
        if row['moisture'] < 30:
            need_irrigation = 1
        
        # High rain probability reduces irrigation need
        if row['rainfall_prob'] > 70:
            need_irrigation = 0
        
        # Flowering stage needs more water
        if row['crop_stage'] == 'flowering' and row['moisture'] < 40:
            need_irrigation = 1
        
        # Sandy soil needs more frequent irrigation
        if row['soil_type'] == 'sandy' and row['moisture'] < 35:
            need_irrigation = 1
        
        # High temperature increases need
        if row['temperature'] > 35 and row['moisture'] < 50:
            need_irrigation = 1
        
        irrigation_required.append(need_irrigation)
    
    df['irrigation_required'] = irrigation_required
    
    print(f"✅ Dataset generated: {len(df)} samples")
    print(f"   - Irrigation required: {sum(irrigation_required)} samples ({sum(irrigation_required)/len(irrigation_required)*100:.1f}%)")
    print(f"   - No irrigation: {len(irrigation_required) - sum(irrigation_required)} samples")
    
    return df


# ============================================================================
# STEP 2: PREPROCESSING
# ============================================================================

class IrrigationPreprocessor:
    """
    Handles all data preprocessing steps:
    - Label encoding for categorical variables
    - Normalization for numeric features
    - Missing value handling
    """
    
    def __init__(self):
        """Initialize encoders and scalers"""
        # Label encoders convert categories to numbers
        # Example: 'clay' -> 0, 'loam' -> 1, 'sandy' -> 2
        self.soil_encoder = LabelEncoder()
        self.stage_encoder = LabelEncoder()
        
        # Scaler normalizes numbers to similar range (0-1)
        # This helps ML models learn better
        self.scaler = StandardScaler()
        
        # Store feature names for later use
        self.feature_names = None
    
    def fit_transform(self, df):
        """
        Learn from the data and transform it.
        Use this for TRAINING data only.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Processed features (X) and target (y)
        """
        print("\n🔄 Preprocessing data...")
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Handle missing values (if any)
        # Fill numeric columns with median (middle value)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Fill categorical columns with mode (most common value)
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
        
        # Encode categorical variables to numbers
        df['soil_type_encoded'] = self.soil_encoder.fit_transform(df['soil_type'])
        df['crop_stage_encoded'] = self.stage_encoder.fit_transform(df['crop_stage'])
        
        # Select features (X) and target (y)
        feature_columns = [
            'soil_type_encoded', 'crop_stage_encoded',
            'nitrogen', 'phosphorus', 'potassium',
            'ph', 'moisture', 'temperature', 'rainfall_prob'
        ]
        
        X = df[feature_columns].values
        y = df['irrigation_required'].values
        
        # Normalize features to standard scale
        # This makes all features have similar importance
        X = self.scaler.fit_transform(X)
        
        # Store feature names for feature importance later
        self.feature_names = feature_columns
        
        print(f"✅ Preprocessing complete")
        print(f"   - Features shape: {X.shape}")
        print(f"   - Target shape: {y.shape}")
        
        return X, y
    
    def transform(self, df):
        """
        Transform new data using previously learned parameters.
        Use this for TEST data or PREDICTION.
        
        Args:
            df: Input DataFrame
        
        Returns:
            Processed features (X)
        """
        df = df.copy()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Encode using already fitted encoders
        df['soil_type_encoded'] = self.soil_encoder.transform(df['soil_type'])
        df['crop_stage_encoded'] = self.stage_encoder.transform(df['crop_stage'])
        
        # Select same features
        feature_columns = [
            'soil_type_encoded', 'crop_stage_encoded',
            'nitrogen', 'phosphorus', 'potassium',
            'ph', 'moisture', 'temperature', 'rainfall_prob'
        ]
        
        X = df[feature_columns].values
        
        # Scale using already fitted scaler
        X = self.scaler.transform(X)
        
        return X


# ============================================================================
# STEP 3: TRAIN MODELS
# ============================================================================

def train_models(X_train, y_train):
    """
    Train two classification models:
    1. Logistic Regression (simple baseline)
    2. Random Forest (more powerful, main model)
    
    Args:
        X_train: Training features
        y_train: Training target
    
    Returns:
        Dictionary containing both trained models
    """
    print("\n🤖 Training models...")
    
    models = {}
    
    # Model 1: Logistic Regression (Baseline)
    # Simple, fast, good for linear relationships
    print("\n   Training Logistic Regression (baseline)...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    models['logistic_regression'] = lr_model
    print("   ✅ Logistic Regression trained")
    
    # Model 2: Random Forest (Main Model)
    # More powerful, can capture complex patterns
    # Uses multiple decision trees for better accuracy
    print("\n   Training Random Forest (main model)...")
    rf_model = RandomForestClassifier(
        n_estimators=100,      # Number of trees in the forest
        max_depth=10,          # Maximum depth of each tree
        random_state=42,       # For reproducibility
        n_jobs=-1              # Use all CPU cores
    )
    rf_model.fit(X_train, y_train)
    models['random_forest'] = rf_model
    print("   ✅ Random Forest trained")
    
    return models


# ============================================================================
# STEP 4: EVALUATE MODELS
# ============================================================================

def evaluate_models(models, X_test, y_test, feature_names):
    """
    Evaluate model performance using multiple metrics.
    
    Metrics explained:
    - Accuracy: Overall correctness (% of correct predictions)
    - Precision: When model says "irrigate", how often is it right?
    - Recall: Of all cases needing irrigation, how many did we catch?
    
    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test target
        feature_names: Names of features
    """
    print("\n📈 Evaluating models...\n")
    
    results = {}
    
    for model_name, model in models.items():
        print(f"{'='*60}")
        print(f"Model: {model_name.upper()}")
        print(f"{'='*60}")
        
        # Make predictions on test set
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Accuracy:  {accuracy:.3f} ({accuracy*100:.1f}%)")
        print(f"   Precision: {precision:.3f} ({precision*100:.1f}%)")
        print(f"   Recall:    {recall:.3f} ({recall*100:.1f}%)")
        
        # Confusion Matrix
        # Shows: [True Negatives, False Positives]
        #        [False Negatives, True Positives]
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n🔢 Confusion Matrix:")
        print(f"   [[TN={cm[0,0]:3d}, FP={cm[0,1]:3d}]")
        print(f"    [FN={cm[1,0]:3d}, TP={cm[1,1]:3d}]]")
        
        # Classification Report (detailed breakdown)
        print(f"\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['No Irrigation', 'Need Irrigation']))
        
        # Feature importance (only for tree-based models)
        if hasattr(model, 'feature_importances_'):
            print(f"\n⭐ Feature Importance (Top 5):")
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1][:5]
            
            for i, idx in enumerate(indices, 1):
                print(f"   {i}. {feature_names[idx]:20s}: {importances[idx]:.4f}")
        
        print()
        
        # Store results
        results[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'confusion_matrix': cm,
            'predictions': y_pred
        }
    
    return results


# ============================================================================
# STEP 5: SAVE MODEL
# ============================================================================

def save_model(model, preprocessor, filename='irrigation_model.pkl'):
    """
    Save trained model and preprocessor to disk.
    This allows us to use the model later without retraining.
    
    Args:
        model: Trained model
        preprocessor: Fitted preprocessor
        filename: Output filename
    """
    print(f"\n💾 Saving model to {filename}...")
    
    # Bundle model and preprocessor together
    model_package = {
        'model': model,
        'preprocessor': preprocessor
    }
    
    # Save using pickle (Python object serialization)
    with open(filename, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"✅ Model saved successfully!")


def load_model(filename='irrigation_model.pkl'):
    """
    Load previously saved model from disk.
    
    Args:
        filename: Model filename
    
    Returns:
        Dictionary with model and preprocessor
    """
    print(f"\n📂 Loading model from {filename}...")
    
    with open(filename, 'rb') as f:
        model_package = pickle.load(f)
    
    print(f"✅ Model loaded successfully!")
    return model_package


# ============================================================================
# STEP 6: PREDICTION FUNCTION
# ============================================================================

def predict_irrigation(
    soil_type,
    crop_stage,
    nitrogen,
    phosphorus,
    potassium,
    ph,
    moisture,
    temperature,
    rainfall_prob,
    model_file='irrigation_model.pkl'
):
    """
    Predict irrigation need for given conditions.
    
    This is the main function to use in production!
    
    Args:
        soil_type: 'clay', 'loam', or 'sandy'
        crop_stage: 'germination', 'vegetative', 'flowering', 'harvest'
        nitrogen: Nitrogen level (ppm)
        phosphorus: Phosphorus level (ppm)
        potassium: Potassium level (ppm)
        ph: Soil pH (5.0-8.5)
        moisture: Soil moisture percentage (0-100)
        temperature: Temperature in Celsius
        rainfall_prob: Rainfall probability (0-100%)
        model_file: Path to saved model
    
    Returns:
        Dictionary with:
        - need_irrigation: Boolean
        - confidence: Prediction confidence (0-1)
        - top_features: Top 3 features affecting decision
    """
    # Load saved model
    package = load_model(model_file)
    model = package['model']
    preprocessor = package['preprocessor']
    
    # Create DataFrame from input
    input_data = pd.DataFrame([{
        'soil_type': soil_type,
        'crop_stage': crop_stage,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'ph': ph,
        'moisture': moisture,
        'temperature': temperature,
        'rainfall_prob': rainfall_prob
    }])
    
    # Preprocess
    X = preprocessor.transform(input_data)
    
    # Predict
    prediction = model.predict(X)[0]
    
    # Get confidence (probability of prediction)
    # predict_proba returns [prob_class_0, prob_class_1]
    probabilities = model.predict_proba(X)[0]
    confidence = probabilities[prediction]
    
    # Get feature importance (top 3)
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:3]
        
        top_features = [
            {
                'feature': preprocessor.feature_names[idx],
                'importance': float(importances[idx])
            }
            for idx in indices
        ]
    else:
        top_features = []
    
    # Return results
    return {
        'need_irrigation': bool(prediction),
        'confidence': float(confidence),
        'probability_irrigation': float(probabilities[1]),
        'probability_no_irrigation': float(probabilities[0]),
        'top_features': top_features
    }


# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

def main_training_pipeline():
    """
    Complete end-to-end training pipeline.
    Run this to train and save the model.
    """
    print("="*70)
    print("🌾 IRRIGATION ML PIPELINE - TRAINING")
    print("="*70)
    
    # Step 1: Generate dataset
    df = generate_sample_dataset(n_samples=1000)
    
    # Show dataset info
    print("\n📋 Dataset Info:")
    print(df.info())
    print("\n📊 First 5 rows:")
    print(df.head())
    
    # Step 2: Preprocess
    preprocessor = IrrigationPreprocessor()
    X, y = preprocessor.fit_transform(df)
    
    # Split into train and test sets
    # 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Data Split:")
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Test set:     {len(X_test)} samples")
    
    # Step 3: Train models
    models = train_models(X_train, y_train)
    
    # Step 4: Evaluate
    results = evaluate_models(models, X_test, y_test, preprocessor.feature_names)
    
    # Step 5: Save best model (Random Forest)
    save_model(models['random_forest'], preprocessor, 'irrigation_model.pkl')
    
    print("\n" + "="*70)
    print("✅ TRAINING PIPELINE COMPLETE!")
    print("="*70)
    
    return models, preprocessor, results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Train the model
    models, preprocessor, results = main_training_pipeline()
    
    # Example prediction after training
    print("\n" + "="*70)
    print("🔮 EXAMPLE PREDICTION")
    print("="*70)
    
    test_prediction = predict_irrigation(
        soil_type='sandy',
        crop_stage='flowering',
        nitrogen=80,
        phosphorus=40,
        potassium=60,
        ph=6.5,
        moisture=25,
        temperature=32,
        rainfall_prob=15
    )
    
    print("\n📊 Prediction Results:")
    print(f"   Need Irrigation: {test_prediction['need_irrigation']}")
    print(f"   Confidence: {test_prediction['confidence']:.2%}")
    print(f"   Irrigation Probability: {test_prediction['probability_irrigation']:.2%}")
    print(f"   No Irrigation Probability: {test_prediction['probability_no_irrigation']:.2%}")
    print(f"\n⭐ Top Features Affecting Decision:")
    for i, feature in enumerate(test_prediction['top_features'], 1):
        print(f"   {i}. {feature['feature']:20s}: {feature['importance']:.4f}")
