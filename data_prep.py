import os
import pandas as pd

# Configuration
DATASET_DIR = 'dataset'
OUTPUT_CSV = 'metadata.csv'

def create_metadata():
    data = []
    
    # Walk through the dataset directory
    if not os.path.exists(DATASET_DIR):
        print(f"Error: '{DATASET_DIR}' folder not found. Please create it and add images.")
        return

    for category in os.listdir(DATASET_DIR):
        cat_path = os.path.join(DATASET_DIR, category)
        
        if os.path.isdir(cat_path):
            for filename in os.listdir(cat_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # Create entry 
                    data.append({
                        'image_name': filename,
                        'source_url': 'Local File', # Placeholder as we are using local files
                        'category': category,
                        'file_path': os.path.join(cat_path, filename)
                    })
    
    # Save to CSV
    df = pd.DataFrame(data)
    if not df.empty:
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"Success! Metadata saved to {OUTPUT_CSV} with {len(df)} images.")
    else:
        print("No images found. Check your folder structure.")

if __name__ == "__main__":
    create_metadata()