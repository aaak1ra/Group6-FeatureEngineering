import pandas as pd
import os
from datetime import datetime

def time_based_feature_extraction(filename):
    """
    Function 2: Extracts useful info from dates (year, month, day, etc.)
    Example: 2024-01-15 → Year=2024, Month=1, Day=15, DayOfWeek=Monday
    """
    print(f"🔄 Processing {filename} - Extracting time features...")
    
    # Read the CSV file
    input_path = os.path.join('input', filename)
    df = pd.read_csv(input_path)
    
    # Look for columns that might contain dates
    date_keywords = ['date', 'time', 'day', 'year', 'month', 'enrollment', 'birth']
    date_columns_found = False
    
    for col in df.columns:
        # Check if column name has date-related words
        if any(keyword in col.lower() for keyword in date_keywords):
            try:
                # Convert to datetime format
                df[col] = pd.to_datetime(df[col])
                
                # Extract various time features [citation:7]
                df[f'{col}_Year'] = df[col].dt.year
                df[f'{col}_Month'] = df[col].dt.month
                df[f'{col}_Day'] = df[col].dt.day
                df[f'{col}_DayOfWeek'] = df[col].dt.day_name()
                df[f'{col}_Quarter'] = 'Q' + df[col].dt.quarter.astype(str)
                
                # Check if it's weekend (Saturday or Sunday)
                df[f'{col}_IsWeekend'] = df[col].dt.dayofweek.isin([5, 6])
                
                # Determine season based on month
                def get_season(month):
                    if month in [12, 1, 2]:
                        return 'Winter'
                    elif month in [3, 4, 5]:
                        return 'Spring'
                    elif month in [6, 7, 8]:
                        return 'Summer'
                    else:
                        return 'Fall'
                
                df[f'{col}_Season'] = df[col].dt.month.apply(get_season)
                date_columns_found = True
                print(f"   ✅ Extracted time features from: {col}")
                
            except Exception as e:
                print(f"   ⚠️ Could not process column '{col}': {str(e)[:50]}...")
    
    if not date_columns_found:
        print("⚠️ No date columns found to process")
    
    # Save to output folder
    output_filename = f'time_features_{filename}'
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
            time_based_feature_extraction(file)