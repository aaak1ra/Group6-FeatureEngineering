import os
import sys
from encode_features import encode_computed_categorical_features
from time_features import time_based_feature_extraction
from bin_ranges import bin_numeric_ranges
from tag_anomalies import tag_anomalies_column

def setup_folders():
    """Create input and output folders if they don't exist"""
    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('tests', exist_ok=True)
    print("📁 Folders ready: input/, output/, tests/")

def process_all_files():
    """Run all 4 functions on every CSV file in the input folder"""
    
    print("\n" + "="*60)
    print("🚀 FEATURE ENGINEERING PIPELINE - GROUP 6")
    print("="*60)
    
    # Check if input folder has CSV files
    csv_files = [f for f in os.listdir('input') if f.endswith('.csv')]
    
    if not csv_files:
        print("\n❌ No CSV files found in 'input' folder!")
        print("📌 Please add CSV files to the 'input' folder and try again.")
        print("\nExample: Create a sample CSV file named 'students.csv' with content:")
        print("""
Name,Age,Score,EnrollmentDate
John,25,85,2024-01-15
Mary,22,92,2024-01-20
Bob,35,45,2024-02-10
Alice,19,150,2024-12-25
        """)
        return
    
    print(f"\n📄 Found {len(csv_files)} CSV file(s) to process:")
    for f in csv_files:
        print(f"   - {f}")
    
    # Process each file with all functions
    for filename in csv_files:
        print(f"\n{'='*40}")
        print(f"📊 PROCESSING: {filename}")
        print(f"{'='*40}")
        
        try:
            # Run all 4 functions
            encode_computed_categorical_features(filename)
            time_based_feature_extraction(filename)
            bin_numeric_ranges(filename)
            tag_anomalies_column(filename)
            
            print(f"\n✅ Completed all processing for {filename}")
        except Exception as e:
            print(f"\n❌ Error processing {filename}: {str(e)}")
            print("Please check your CSV file format.")
    
    print("\n" + "="*60)
    print("🎉 ALL PROCESSING COMPLETE!")
    print("📁 Check the 'output' folder for results")
    print("="*60)

if __name__ == "__main__":
    setup_folders()
    process_all_files()
    
    # Ask if user wants to see output files
    response = input("\n📂 View output files? (y/n): ")
    if response.lower() == 'y':
        output_files = os.listdir('output')
        if output_files:
            print("\n📁 Output files created:")
            for f in output_files:
                size = os.path.getsize(os.path.join('output', f))
                print(f"   - {f} ({size} bytes)")
        else:
            print("No output files yet.")