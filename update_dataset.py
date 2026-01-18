#!/usr/bin/env python3
"""
Update Dataset from Kaggle
Downloads and integrates the latest disease and symptoms dataset from Kaggle
"""

import os
import sys
import json
import pandas as pd
from collections import defaultdict

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import kagglehub
        import pandas as pd
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing required packages...")
        
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub", "pandas"])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please install manually:")
            print("pip install kagglehub pandas")
            return False

def download_kaggle_dataset():
    """Download the latest dataset from Kaggle."""
    try:
        import kagglehub
        
        print("📥 Downloading dataset from Kaggle...")
        print("Dataset: choongqianzheng/disease-and-symptoms-dataset")
        
        # Download latest version
        path = kagglehub.dataset_download("choongqianzheng/disease-and-symptoms-dataset")
        print(f"✅ Dataset downloaded to: {path}")
        return path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("💡 Make sure you have Kaggle API credentials configured")
        print("   Visit: https://www.kaggle.com/docs/api")
        return None

def process_kaggle_data(dataset_path):
    """Process the downloaded Kaggle dataset."""
    print("🔄 Processing Kaggle dataset...")
    
    # Find CSV files
    csv_files = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    
    if not csv_files:
        print("❌ No CSV files found in dataset")
        return None, None, None
    
    print(f"📄 Found CSV files: {[os.path.basename(f) for f in csv_files]}")
    
    # Process symptoms and diseases
    symptom_to_disease = {}
    disease_symptoms = defaultdict(set)
    disease_precautions = {}
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file).lower()
        
        try:
            df = pd.read_csv(csv_file)
            print(f"📊 Processing {filename}: {df.shape[0]} rows, {df.shape[1]} columns")
            
            if 'disease' in df.columns.str.lower():
                # Find disease column
                disease_col = None
                for col in df.columns:
                    if col.lower() == 'disease':
                        disease_col = col
                        break
                
                if disease_col:
                    # Process symptoms file
                    if 'symptom' in filename:
                        symptom_cols = [col for col in df.columns if col.startswith('Symptom_')]
                        
                        for _, row in df.iterrows():
                            disease = str(row[disease_col]).lower().strip()
                            
                            for symptom_col in symptom_cols:
                                if pd.notna(row[symptom_col]):
                                    symptom = str(row[symptom_col]).lower().strip()
                                    symptom = symptom.replace('_', ' ')
                                    
                                    if symptom and symptom != 'nan':
                                        symptom_to_disease[symptom] = disease
                                        disease_symptoms[disease].add(symptom)
                    
                    # Process precautions file
                    elif 'precaution' in filename:
                        precaution_cols = [col for col in df.columns if col.startswith('Precaution_')]
                        
                        for _, row in df.iterrows():
                            disease = str(row[disease_col]).lower().strip()
                            precautions = []
                            
                            for precaution_col in precaution_cols:
                                if pd.notna(row[precaution_col]):
                                    precaution = str(row[precaution_col]).strip()
                                    if precaution and precaution != 'nan':
                                        precautions.append(precaution)
                            
                            if precautions:
                                disease_precautions[disease] = precautions
            
        except Exception as e:
            print(f"⚠️  Error processing {filename}: {e}")
            continue
    
    return symptom_to_disease, disease_symptoms, disease_precautions

def backup_existing_data():
    """Create backup of existing data files."""
    backup_files = []
    
    for filename in ['data/symptoms.json', 'data/remedies.json']:
        if os.path.exists(filename):
            backup_name = filename.replace('.json', '_backup.json')
            
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                with open(backup_name, 'w') as f:
                    json.dump(data, f, indent=2)
                
                backup_files.append(backup_name)
                print(f"💾 Backed up {filename} to {backup_name}")
                
            except Exception as e:
                print(f"⚠️  Could not backup {filename}: {e}")
    
    return backup_files

def update_system_data(symptom_to_disease, disease_symptoms, disease_precautions):
    """Update the system's data files with new Kaggle data."""
    print("📝 Updating system data files...")
    
    # Load existing symptoms
    existing_symptoms = {}
    try:
        with open('data/symptoms.json', 'r') as f:
            existing_data = json.load(f)
        existing_symptoms = existing_data.get('symptom_map', {})
    except FileNotFoundError:
        print("📄 No existing symptoms.json found, creating new one")
    except Exception as e:
        print(f"⚠️  Error loading existing symptoms: {e}")
    
    # Merge symptom mappings (keep existing, add new)
    merged_symptoms = {**symptom_to_disease, **existing_symptoms}
    
    # Update symptoms.json
    updated_symptoms_data = {
        "symptom_map": merged_symptoms,
        "disease_symptoms": {k: list(v) for k, v in disease_symptoms.items()},
        "total_diseases": len(disease_symptoms),
        "last_updated": pd.Timestamp.now().isoformat()
    }
    
    with open('data/symptoms.json', 'w') as f:
        json.dump(updated_symptoms_data, f, indent=2)
    
    # Load existing remedies
    existing_remedies = {}
    emergency_symptoms = []
    try:
        with open('data/remedies.json', 'r') as f:
            existing_remedies_data = json.load(f)
        existing_remedies = existing_remedies_data.get('remedy_database', {})
        emergency_symptoms = existing_remedies_data.get('emergency_symptoms', [])
    except FileNotFoundError:
        print("📄 No existing remedies.json found, keeping current structure")
    except Exception as e:
        print(f"⚠️  Error loading existing remedies: {e}")
    
    # Update remedies.json with precautions
    updated_remedies_data = {
        "remedy_database": existing_remedies,
        "emergency_symptoms": emergency_symptoms,
        "disease_precautions": disease_precautions,
        "last_updated": pd.Timestamp.now().isoformat()
    }
    
    with open('data/remedies.json', 'w') as f:
        json.dump(updated_remedies_data, f, indent=2)
    
    return len(merged_symptoms), len(disease_precautions)

def main():
    """Main function to update dataset."""
    print("🏥 AI Medical Diagnosis System - Dataset Updater")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Backup existing data
    backup_files = backup_existing_data()
    
    try:
        # Download dataset
        dataset_path = download_kaggle_dataset()
        if not dataset_path:
            return 1
        
        # Process dataset
        symptom_to_disease, disease_symptoms, disease_precautions = process_kaggle_data(dataset_path)
        
        if not symptom_to_disease:
            print("❌ No symptom data extracted from dataset")
            return 1
        
        # Update system data
        total_symptoms, total_precautions = update_system_data(
            symptom_to_disease, disease_symptoms, disease_precautions
        )
        
        print("\n" + "=" * 60)
        print("✅ DATASET UPDATE COMPLETE!")
        print("=" * 60)
        print(f"📊 Total symptom mappings: {total_symptoms}")
        print(f"🏥 Total diseases: {len(disease_symptoms)}")
        print(f"⚠️  Total precaution sets: {total_precautions}")
        
        if backup_files:
            print(f"💾 Backup files created: {len(backup_files)}")
        
        print("\n🎉 Your AI Medical Diagnosis System is now updated!")
        print("🚀 Test it with: python chatgpt_interface.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        
        # Restore backups if something went wrong
        if backup_files:
            print("🔄 Attempting to restore from backup...")
            for backup_file in backup_files:
                try:
                    original_file = backup_file.replace('_backup.json', '.json')
                    os.rename(backup_file, original_file)
                    print(f"✅ Restored {original_file}")
                except Exception as restore_error:
                    print(f"❌ Could not restore {backup_file}: {restore_error}")
        
        return 1

if __name__ == "__main__":
    exit(main())