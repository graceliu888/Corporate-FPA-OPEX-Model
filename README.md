# Corporate FP&A — Cost Center OPEX Model

This project replicates a real-world Corporate FP&A workflow for managing cost center OPEX budgets, forecasts, and variance analysis. It is designed based on processes from large matrix organizations such as IBM, Roche, and Fortune 500 finance teams.（Public Data Set）

---

## 📊 Key Features

### **1. Automated Variance Analysis**
- Budget vs Actual
- Forecast vs Actual
- Budget vs Forecast
- Summaries by cost center

### **2. Driver-Based OPEX Components**
Includes breakdowns for:
- Travel
- Software
- Vendor Spend
- Office Expense
- Headcount-related costs

### **3. Power BI Dashboard**
- Month-over-month variance
- OPEX category trends
- Forecast accuracy tracking
- Cost center drill-downs

### **4. FP&A Python Models**
- Variance engine  
- Forecast pipeline  
- Report automation scripts  

### **5. Realistic Enterprise Data Structure**
The dataset simulates a real multi-function corporate environment:
- HR  
- IT  
- Finance  
- Legal  
- Operations  

---

## 📁 Project Structure

```
OPEX Dashboard/
├── data/                          # OPEX dataset (CSV)
│   ├── opex_cost_center_data.csv  # Input data
│   ├── opex_processed_for_powerbi.csv  # Processed data (generated)
│   ├── opex_costcenter_summary.csv     # Summary by cost center (generated)
│   └── opex_with_forecast.csv          # Forecast data (generated)
├── models/                        # Python financial models
│   ├── opex_model.py             # Core OPEX calculations
│   ├── forecast_model.py         # Forecasting models
│   └── allocation_model.py        # Cost allocation model
├── scripts/                       # Execution scripts
│   ├── variance_analysis.py      # Variance calculation script
│   ├── forecast_pipeline.py       # Forecast generation script
│   └── run_all.py                # Full pipeline runner
├── dashboards/                    # Power BI dashboard
│   └── OPEX_FPA_Dashboard.pbix
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "C:\Users\user\Desktop\FP&A Projects\OPEX Dashboard"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- pandas (>=1.5.0)
- numpy (>=1.23.0)
- matplotlib (>=3.6.0)
- seaborn (>=0.12.0)
- jupyter (>=1.0.0)

---

## 💻 Usage

### Option 1: Run Full Pipeline (Recommended)
Run both variance analysis and forecast generation in one command:

```bash
python scripts/run_all.py
```

### Option 2: Run Individual Scripts

**Step 1: Variance Analysis**
```bash
python scripts/variance_analysis.py
```
This generates:
- `data/opex_processed_for_powerbi.csv` - Processed data with variances
- `data/opex_costcenter_summary.csv` - Summary by cost center

**Step 2: Forecast Generation**
```bash
python scripts/forecast_pipeline.py
```
This generates:
- `data/opex_with_forecast.csv` - Data with run-rate and growth forecasts

### Option 3: Use Models Programmatically
```python
from models.opex_model import OPEXModel
from pathlib import Path

# Load and process data
model = OPEXModel.from_csv("data/opex_cost_center_data.csv")
processed_df = model.get_processed_frame()
summary_df = model.summarize_by_cost_center()
```

---

## 📋 Data Requirements

The input CSV file (`data/opex_cost_center_data.csv`) must contain the following columns:

**Required Columns:**
- `CostCenter` - Cost center name (e.g., "HR", "IT", "Finance")
- `Month` - Month in YYYY-MM format (e.g., "2024-01")
- `Budget` - Budgeted amount
- `Forecast` - Forecasted amount
- `Actuals` - Actual amount
- `Travel` - Travel expenses
- `Software` - Software expenses
- `VendorSpend` - Vendor spending
- `OfficeExpense` - Office expenses
- `Headcount` - Number of employees (optional, used for allocation)

---

## 🛠 Tools & Technologies
- Python (Pandas, NumPy)
- Power BI
- Excel
- GitHub
- FP&A variance methodology

---

## ⚠️ Error Handling

The project includes comprehensive error handling:
- **File validation**: Checks if input files exist
- **Data validation**: Validates required columns are present
- **Empty data checks**: Prevents processing empty datasets
- **Clear error messages**: Provides helpful error messages for troubleshooting

---

## 🚀 Future Enhancements
- Rolling Forecast model
- Machine Learning forecast (Prophet)
- YTD variance dashboard
- Cost allocation engine
- Unit tests and integration tests
- Configuration file for parameters
- Logging framework



