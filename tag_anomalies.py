import pandas as pd
import os
import numpy as np

def tag_anomalies_column(filename):
    """
    Function 4: Finds and flags unusual/weird data
    Example: Age = 200 or Salary = -5000 would be flagged as anomalies
    """
    print(f"🔄 Processing {filename} - Tagging anomalies...")
    
    # Read the CSV file
    input_path = os.path.join('input', filename)
    df = pd.read_csv(input_path)
    
    # Create columns for anomaly flags
    df['Has_Anomaly'] = 'No'
    df['Anomaly_Details'] = ''
    
    # Find all numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    anomaly_count = 0
    
    for col in numeric_cols:
        # Skip ID columns
        if col.lower() in ['id', 'studentid', 'employeeid', 'index']:
            continue
            
        try:
            # Calculate statistics
            Q1 = df[col].quantile(0.25)  # First quartile (25th percentile)
            Q3 = df[col].quantile(0.75)  # Third quartile (75th percentile)
            IQR = Q3 - Q1  # Interquartile range
            
            # Define boundaries for normal values [citation:7]
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Check each value
            for idx, value in df[col].items():
                if pd.notna(value):  # Skip if value is missing
                    if value < lower_bound:
                        df.loc[idx, 'Has_Anomaly'] = 'Yes'
                        df.loc[idx, 'Anomaly_Details'] += f'{col} is too low; '
                        anomaly_count += 1
                    elif value > upper_bound:
                        df.loc[idx, 'Has_Anomaly'] = 'Yes'
                        df.loc[idx, 'Anomaly_Details'] += f'{col} is too high; '
                        anomaly_count += 1
            
            # Also check for negative values in columns that shouldn't be negative
            if any(word in col.lower() for word in ['age', 'score', 'grade', 'price', 'salary']):
                negative_mask = df[col] < 0
                if negative_mask.any():
                    df.loc[negative_mask, 'Has_Anomaly'] = 'Yes'
                    df.loc[negative_mask, 'Anomaly_Details'] += f'{col} is negative; '
                    anomaly_count += negative_mask.sum()
                    
        except Exception as e:
            print(f"   ⚠️ Error checking column '{col}': {str(e)[:50]}...")
    
    if anomaly_count == 0:
        print("   ✅ No anomalies detected")
    else:
        print(f"   ⚠️ Found {anomaly_count} potential anomalies")
    
    # Save to output folder
    output_filename = f'anomalies_{filename}'
    output_path = os.path.join('output', output_filename)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Saved to {output_path}")
    return output_filename

if __name__ == "__main__":
    if not os.path.exists('input'):
        os.makedirs('input')
        print("📁 Created 'input' folder. Place your CSV files there.")
    
    for file in os.listdir('input'):
        if file.endswith('.csv'):
            tag_anomalies_column(file)