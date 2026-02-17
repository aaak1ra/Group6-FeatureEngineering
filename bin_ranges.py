import pandas as pd
import os
import numpy as np

def bin_numeric_ranges(filename):
    """
    Function 3: Groups numbers into categories/buckets
    Example: Age 15 → "Child", Age 25 → "Young Adult", Age 45 → "Middle Age"
    """
    print(f"🔄 Processing {filename} - Binning numeric ranges...")
    
    # Read the CSV file
    input_path = os.path.join('input', filename)
    df = pd.read_csv(input_path)
    
    # Find all numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    binned_count = 0
    
    for col in numeric_cols:
        # Skip ID columns (usually don't want to bin these)
        if col.lower() in ['id', 'studentid', 'employeeid', 'index']:
            continue
            
        try:
            # For Age-like columns (0-100 range)
            if 'age' in col.lower():
                bins = [0, 18, 30, 50, 100]
                labels = ['Child/Teen', 'Young Adult', 'Adult', 'Senior']
                df[f'{col}_Group'] = pd.cut(df[col], bins=bins, labels=labels)
                binned_count += 1
                
            # For Score/Grade columns (0-100 range)
            elif any(word in col.lower() for word in ['score', 'grade', 'percentage']):
                bins = [0, 60, 70, 85, 100]
                labels = ['Failing', 'Average', 'Good', 'Excellent']
                df[f'{col}_Grade'] = pd.cut(df[col], bins=bins, labels=labels)
                binned_count += 1
                
            # For Salary/Price columns (wider range)
            elif any(word in col.lower() for word in ['salary', 'price', 'amount', 'cost']):
                # Create 4 equal groups based on the data
                try:
                    df[f'{col}_Category'] = pd.qcut(df[col], q=4, 
                                                     labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
                    binned_count += 1
                except:
                    # If qcut fails, use cut with equal width
                    df[f'{col}_Category'] = pd.cut(df[col], bins=4, 
                                                    labels=['Q1', 'Q2', 'Q3', 'Q4'])
                    binned_count += 1
                    
            # For other numeric columns, create 3 groups
            else:
                df[f'{col}_Bin'] = pd.cut(df[col], bins=3, 
                                           labels=['Low', 'Medium', 'High'])
                binned_count += 1
                
            print(f"   ✅ Binned column: {col}")
                
        except Exception as e:
            print(f"   ⚠️ Could not bin column '{col}': {str(e)[:50]}...")
    
    if binned_count == 0:
        print("⚠️ No numeric columns were binned")
    
    # Save to output folder
    output_filename = f'binned_{filename}'
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
            bin_numeric_ranges(file)