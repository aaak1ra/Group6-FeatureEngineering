import pandas as pd
import os
import numpy as np

def encode_computed_categorical_features(filename):
    """
    Function 1: Converts text categories into numbers (One-Hot Encoding)
    Example: Color: Red, Blue, Green → Color_Red=1, Color_Blue=0, Color_Green=0
    """
    print(f"🔄 Processing {filename} - Encoding categorical features...")
    
    # Read the CSV file from input folder
    input_path = os.path.join('input', filename)
    df = pd.read_csv(input_path)
    
    # Find all text columns (categorical data)
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    if len(categorical_cols) == 0:
        print("⚠️ No categorical columns found to encode")
    else:
        # Create dummy variables for each categorical column
        for col in categorical_cols:
            # This creates 1s and 0s for each category
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, dummies], axis=1)
            print(f"   ✅ Encoded column: {col}")
    
    # Save to output folder
    output_filename = f'encoded_{filename}'
    output_path = os.path.join('output', output_filename)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Saved to {output_path}")
    return output_filename

# This runs automatically when you run the file
if __name__ == "__main__":
    # Check if input folder exists
    if not os.path.exists('input'):
        os.makedirs('input')
        print("📁 Created 'input' folder. Place your CSV files there.")
    
    # Process all CSV files in input folder
    for file in os.listdir('input'):
        if file.endswith('.csv'):
            encode_computed_categorical_features(file)