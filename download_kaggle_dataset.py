#!/usr/bin/env python3
"""
Simple Kaggle Dataset Downloader
Downloads the disease and symptoms dataset from Kaggle
"""

try:
    import kagglehub
except ImportError:
    print("❌ kagglehub not installed. Installing...")
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kagglehub"])
        import kagglehub
        print("✅ kagglehub installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install kagglehub. Please install manually:")
        print("pip install kagglehub")
        exit(1)

try:
    # Download latest version
    print("📥 Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("choongqianzheng/disease-and-symptoms-dataset")
    print("Path to dataset files:", path)

    # List the files in the dataset
    import os
    print("\nDataset contents:")
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"  📄 {file} ({file_size:,} bytes)")

    print(f"\n✅ Dataset downloaded successfully!")
    print(f"📁 Location: {path}")
    print(f"🔄 To integrate with the AI system, run: python update_dataset.py")

except Exception as e:
    print(f"❌ Error downloading dataset: {e}")
    print("💡 Make sure you have Kaggle API credentials configured")
    print("   Visit: https://www.kaggle.com/docs/api")
    exit(1)