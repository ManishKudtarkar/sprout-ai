# Dataset Management Guide

## 📊 About the Kaggle Dataset

The AI Medical Diagnosis System uses the **"Disease and Symptoms Dataset"** by Choong Qian Zheng from Kaggle, which contains:

- **4,920 symptom-disease mappings**
- **41 unique medical conditions**
- **Evidence-based precautions** for each condition
- **Structured CSV format** for easy processing

## 🔄 Two Ways to Use Kaggle Data

### 1. **Automated Integration** (Recommended)
```bash
python update_dataset.py
```

**What it does:**
- ✅ Downloads latest dataset from Kaggle
- ✅ Processes and cleans the data
- ✅ Merges with existing system data
- ✅ Creates backups of current data
- ✅ Updates both symptoms.json and remedies.json
- ✅ Handles errors gracefully with restore functionality

### 2. **Manual Download** (For exploration)
```bash
python download_kaggle_dataset.py
```

**What it does:**
- ✅ Downloads dataset to local cache
- ✅ Shows file contents and sizes
- ✅ Provides path for manual exploration
- ✅ Installs dependencies automatically

## 📋 Dataset Structure

The Kaggle dataset contains two main files:

### **DiseaseAndSymptoms.csv**
```
Disease, Symptom_1, Symptom_2, ..., Symptom_17
Fungal infection, itching, skin_rash, nodal_skin_eruptions, ...
Allergy, continuous_sneezing, shivering, chills, ...
```

### **Disease precaution.csv**
```
Disease, Precaution_1, Precaution_2, Precaution_3, Precaution_4
Drug Reaction, stop irritation, consult doctor, stop taking drug, follow up
Malaria, Consult nearest hospital, avoid fatty spicy food, avoid non veg food, keep mosquitos out
```

## 🔧 How Integration Works

1. **Download**: Gets latest dataset from Kaggle API
2. **Process**: Extracts symptoms and maps to diseases
3. **Clean**: Normalizes text (underscores → spaces, lowercase)
4. **Merge**: Combines with existing system data (preserves custom mappings)
5. **Update**: Writes to `data/symptoms.json` and `data/remedies.json`
6. **Backup**: Creates backup files before any changes

## 📈 Before vs After Integration

### **Before** (Default System)
- 15 basic symptom mappings
- 6 common conditions
- Basic natural remedies

### **After** (With Kaggle Dataset)
- 161+ symptom mappings
- 41 medical conditions
- Evidence-based precautions
- Enhanced natural remedies

## 🔑 Kaggle API Setup

To use the dataset features, you need Kaggle API credentials:

1. **Create Kaggle Account**: Visit [kaggle.com](https://www.kaggle.com)
2. **Get API Token**: Go to Account → API → Create New API Token
3. **Install Credentials**: 
   - **Windows**: Place `kaggle.json` in `C:\Users\{username}\.kaggle\`
   - **Linux/Mac**: Place `kaggle.json` in `~/.kaggle/`
4. **Set Permissions**: `chmod 600 ~/.kaggle/kaggle.json` (Linux/Mac)

## 🚨 Error Handling

The scripts include comprehensive error handling:

- **Missing Dependencies**: Auto-installs kagglehub and pandas
- **API Errors**: Clear instructions for credential setup
- **Data Corruption**: Automatic backup and restore
- **Network Issues**: Graceful failure with helpful messages

## 💡 Pro Tips

- **Run periodically**: Dataset may get updated with new conditions
- **Check backups**: Backup files are created before any changes
- **Test after update**: Run `python test_system.py` after updating
- **Custom data**: Your custom symptom mappings are preserved during updates