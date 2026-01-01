"""
Soil Moisture Prediction Model using Random Forest Regressor

This script generates synthetic soil moisture data and trains a lightweight ML model.
IMPORTANT: Replace synthetic data generation with real sensor data when available.

Dataset Features:
- soil_type: Type of soil (Sandy, Clay, Loamy, Silt)
- rainfall: Recent rainfall in mm
- humidity: Air humidity percentage
- temperature: Temperature in Celsius
- crop: Type of crop being grown
- moisture_output: Target variable - soil moisture percentage (0-100)

Author: AgroSmart Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import warnings

warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)


def generate_synthetic_dataset(n_samples=2000):
    """
    Generate synthetic soil moisture dataset.
    
    TODO: Replace this function with real data loading when sensor data is available.
    Example: df = pd.read_csv('real_soil_data.csv')
    
    Args:
        n_samples: Number of samples to generate (default: 2000)
    
    Returns:
        pandas.DataFrame: Synthetic dataset with soil moisture data
    """
    print(f"🔄 Generating {n_samples} synthetic samples...")
    
    # Define categories
    soil_types = ['Sandy', 'Clay', 'Loamy', 'Silt']
    crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize', 'Vegetables']
    
    # Generate random features
    data = {
        # Soil type affects water retention
        'soil_type': np.random.choice(soil_types, n_samples),
        
        # Rainfall in mm (0-100mm range)
        'rainfall': np.random.uniform(0, 100, n_samples),
        
        # Humidity percentage (30-100%)
        'humidity': np.random.uniform(30, 100, n_samples),
        
        # Temperature in Celsius (15-45°C)
        'temperature': np.random.uniform(15, 45, n_samples),
        
        # Crop type affects water requirements
        'crop': np.random.choice(crops, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic moisture output based on features
    # This is a simplified model - real relationships are more complex
    moisture = np.zeros(n_samples)
    
    for i in range(n_samples):
        base_moisture = 50  # Base moisture level
        
        # Soil type effect (Clay retains more water, Sandy less)
        soil_effect = {
            'Clay': 15,
            'Loamy': 10,
            'Silt': 5,
            'Sandy': -10
        }
        base_moisture += soil_effect[df.iloc[i]['soil_type']]
        
        # Rainfall effect (more rain = more moisture)
        base_moisture += df.iloc[i]['rainfall'] * 0.2
        
        # Humidity effect (higher humidity = slightly more moisture)
        base_moisture += (df.iloc[i]['humidity'] - 50) * 0.1
        
        # Temperature effect (higher temp = evaporation = less moisture)
        base_moisture -= (df.iloc[i]['temperature'] - 25) * 0.3
        
        # Crop effect (different crops have different water needs)
        crop_effect = {
            'Rice': 5,
            'Sugarcane': 3,
            'Vegetables': 0,
            'Cotton': -2,
            'Wheat': -3,
            'Maize': -1
        }
        base_moisture += crop_effect[df.iloc[i]['crop']]
        
        # Add some random noise to simulate real-world variability
        noise = np.random.normal(0, 5)
        base_moisture += noise
        
        # Ensure moisture is between 0 and 100
        moisture[i] = np.clip(base_moisture, 0, 100)
    
    df['moisture_output'] = moisture
    
    print(f"✅ Dataset generated successfully!")
    print(f"📊 Dataset shape: {df.shape}")
    print(f"📋 Columns: {list(df.columns)}")
    
    return df


def prepare_data(df):
    """
    Prepare data for machine learning by encoding categorical variables.
    
    Args:
        df: pandas DataFrame with raw data
    
    Returns:
        X: Feature matrix
        y: Target variable
        encoders: Dictionary of label encoders for inverse transformation
    """
    print("\n🔄 Preparing data for training...")
    
    # Separate features and target
    X = df.drop('moisture_output', axis=1)
    y = df['moisture_output']
    
    # Encode categorical variables
    # IMPORTANT: When using real data, save these encoders to handle new predictions
    encoders = {}
    
    for column in ['soil_type', 'crop']:
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])
        encoders[column] = le
    
    print(f"✅ Data prepared successfully!")
    print(f"📊 Features shape: {X.shape}")
    print(f"📊 Target shape: {y.shape}")
    
    return X, y, encoders


def train_model(X, y):
    """
    Train Random Forest Regressor model.
    
    Random Forest is chosen because:
    - Lightweight (no GPU needed)
    - Handles non-linear relationships well
    - Works well with small to medium datasets
    - Resistant to overfitting
    - Fast training and prediction
    
    Args:
        X: Feature matrix
        y: Target variable
    
    Returns:
        model: Trained model
        X_test: Test features
        y_test: Test targets
        y_pred: Predictions on test set
    """
    print("\n🔄 Splitting data into train/test sets (80/20 split)...")
    
    # Split data: 80% training, 20% testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Training set size: {X_train.shape[0]} samples")
    print(f"📊 Test set size: {X_test.shape[0]} samples")
    
    print("\n🔄 Training Random Forest Regressor...")
    
    # Initialize Random Forest model
    # n_estimators: Number of trees in the forest
    # max_depth: Maximum depth of trees (prevents overfitting)
    # random_state: For reproducibility
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1  # Use all CPU cores
    )
    
    # Train the model
    model.fit(X_train, y_train)
    
    print("✅ Model trained successfully!")
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    return model, X_test, y_test, y_pred


def evaluate_model(y_test, y_pred):
    """
    Evaluate model performance using RMSE and R² metrics.
    
    Metrics:
    - RMSE (Root Mean Squared Error): Average prediction error in same units as target
    - R² Score: Proportion of variance explained by model (0-1, higher is better)
    
    Args:
        y_test: True values
        y_pred: Predicted values
    """
    print("\n📊 Evaluating model performance...")
    
    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Calculate R² score
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n{'='*50}")
    print(f"🎯 MODEL EVALUATION RESULTS")
    print(f"{'='*50}")
    print(f"📉 RMSE (Root Mean Squared Error): {rmse:.4f}%")
    print(f"📈 R² Score (Coefficient of Determination): {r2:.4f}")
    print(f"{'='*50}")
    
    # Interpretation
    print("\n💡 Interpretation:")
    print(f"   - Average prediction error: ±{rmse:.2f}% moisture")
    
    if r2 >= 0.9:
        print(f"   - R² Score: Excellent! Model explains {r2*100:.1f}% of variance")
    elif r2 >= 0.7:
        print(f"   - R² Score: Good! Model explains {r2*100:.1f}% of variance")
    elif r2 >= 0.5:
        print(f"   - R² Score: Moderate. Model explains {r2*100:.1f}% of variance")
    else:
        print(f"   - R² Score: Needs improvement. Only explains {r2*100:.1f}% of variance")
    
    return rmse, r2


def save_model(model, encoders, filename='soil_model.pkl'):
    """
    Save trained model and encoders to disk.
    
    Args:
        model: Trained ML model
        encoders: Dictionary of label encoders
        filename: Output filename (default: soil_model.pkl)
    """
    print(f"\n🔄 Saving model to '{filename}'...")
    
    # Save both model and encoders together
    model_data = {
        'model': model,
        'encoders': encoders,
        'feature_names': ['soil_type', 'rainfall', 'humidity', 'temperature', 'crop']
    }
    
    with open(filename, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"✅ Model saved successfully!")


def load_model(filename='soil_model.pkl'):
    """
    Load trained model from disk.
    
    Args:
        filename: Model file path
    
    Returns:
        Dictionary containing model, encoders, and feature names
    """
    with open(filename, 'rb') as f:
        model_data = pickle.load(f)
    return model_data


def predict_soil_moisture(soil_type, rainfall, humidity, temperature, crop, model_file='soil_model.pkl'):
    """
    Predict soil moisture based on input parameters.
    
    This is the main function to use for predictions in production.
    
    Args:
        soil_type (str): Type of soil - 'Sandy', 'Clay', 'Loamy', or 'Silt'
        rainfall (float): Recent rainfall in mm (0-100)
        humidity (float): Air humidity percentage (0-100)
        temperature (float): Temperature in Celsius (15-45)
        crop (str): Type of crop - 'Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize', 'Vegetables'
        model_file (str): Path to saved model file
    
    Returns:
        float: Predicted soil moisture percentage (0-100)
    
    Example:
        >>> moisture = predict_soil_moisture('Loamy', 25, 65, 28, 'Rice')
        >>> print(f"Predicted soil moisture: {moisture:.2f}%")
    """
    # Load model and encoders
    model_data = load_model(model_file)
    model = model_data['model']
    encoders = model_data['encoders']
    
    # Create input DataFrame
    input_data = pd.DataFrame({
        'soil_type': [soil_type],
        'rainfall': [rainfall],
        'humidity': [humidity],
        'temperature': [temperature],
        'crop': [crop]
    })
    
    # Encode categorical variables
    input_data['soil_type'] = encoders['soil_type'].transform(input_data['soil_type'])
    input_data['crop'] = encoders['crop'].transform(input_data['crop'])
    
    # Make prediction
    moisture = model.predict(input_data)[0]
    
    # Ensure output is within valid range
    moisture = np.clip(moisture, 0, 100)
    
    return moisture


def main():
    """
    Main pipeline: Generate data -> Train model -> Evaluate -> Save
    """
    print("=" * 60)
    print("🌱 SOIL MOISTURE PREDICTION MODEL - TRAINING PIPELINE")
    print("=" * 60)
    
    # Step 1: Generate synthetic dataset
    # TODO: Replace with real data loading
    df = generate_synthetic_dataset(n_samples=2000)
    
    # Save dataset to CSV for reference
    csv_filename = 'soil_moisture_dataset.csv'
    df.to_csv(csv_filename, index=False)
    print(f"💾 Dataset saved to '{csv_filename}'")
    
    # Step 2: Prepare data
    X, y, encoders = prepare_data(df)
    
    # Step 3: Train model
    model, X_test, y_test, y_pred = train_model(X, y)
    
    # Step 4: Evaluate model
    rmse, r2 = evaluate_model(y_test, y_pred)
    
    # Step 5: Save model
    save_model(model, encoders)
    
    # Step 6: Test prediction function
    print("\n" + "=" * 60)
    print("🧪 TESTING PREDICTION FUNCTION")
    print("=" * 60)
    
    test_cases = [
        {'soil_type': 'Loamy', 'rainfall': 25, 'humidity': 65, 'temperature': 28, 'crop': 'Rice'},
        {'soil_type': 'Sandy', 'rainfall': 10, 'humidity': 45, 'temperature': 35, 'crop': 'Wheat'},
        {'soil_type': 'Clay', 'rainfall': 50, 'humidity': 80, 'temperature': 22, 'crop': 'Sugarcane'}
    ]
    
    for i, test in enumerate(test_cases, 1):
        moisture = predict_soil_moisture(**test)
        print(f"\n📊 Test Case {i}:")
        print(f"   Soil: {test['soil_type']}, Rainfall: {test['rainfall']}mm, "
              f"Humidity: {test['humidity']}%, Temp: {test['temperature']}°C, Crop: {test['crop']}")
        print(f"   ➡️  Predicted Moisture: {moisture:.2f}%")
    
    print("\n" + "=" * 60)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. Replace synthetic data with real sensor data")
    print("   2. Retrain model with actual field measurements")
    print("   3. Integrate predict_soil_moisture() into your application")
    print("   4. Monitor model performance and retrain periodically")
    print("\n💡 Usage Example:")
    print("   from soil_moisture_model import predict_soil_moisture")
    print("   moisture = predict_soil_moisture('Loamy', 25, 65, 28, 'Rice')")
    print("   print(f'Soil moisture: {moisture:.2f}%')")
    

if __name__ == "__main__":
    main()
