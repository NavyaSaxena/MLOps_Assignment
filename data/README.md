## Data Pipeline

### Cleaned Dataset & Download Script/Instructions 

**Cleaned dataset and download script/instructions"** 

**1. Cleaned Dataset (`data/processed/heart_disease_cleaned.csv`)**

303 rows × 14 columns (ready for ML training)
├── 14 standard UCI Heart Disease features (Task 1)
├── Missing values imputed (mean for numeric, mode for categorical)
├── Target converted: multi-class 'num' → binary 'target' (0=No disease, 1=Disease)
└── Production-ready: exact same preprocessing as training pipeline


**2. Raw Dataset (`data/raw/heart_disease_uci.csv`)**
303 rows × 76 columns (original UCI dataset)
└── Downloaded automatically via ucimlrepo.fetch_ucirepo(id=45)


**3. Automated Download & Cleaning Script (`src/data.py`)**
- Single command execution: `python src/data.py`
- **Reproducible:** Always fetches fresh data from UCI + applies your exact Task 1 cleaning
- **Caching:** Saves both raw + processed CSVs for instant reuse
- **Self-documenting:** Prints data shape, target balance, file locations

### Usage Instructions

```bash
# Step 1: Run data pipeline (downloads + cleans automatically)
python src/data.py
```

### Files Generated

data/
├── raw/
│   └── heart_disease_uci.csv          ← Original UCI (76 cols)
└── processed/
    └── heart_disease_cleaned.csv      ← Cleaned ML-ready (14 cols + target)