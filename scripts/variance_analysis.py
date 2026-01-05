"""
Script to:
1) Load OPEX data
2) Run variance calculations
3) Export processed data for Power BI
"""

import sys
import pandas as pd
from pathlib import Path
from models.opex_model import OPEXModel

DATA_PATH = Path("data") / "opex_cost_center_data.csv"
OUTPUT_PATH = Path("data") / "opex_processed_for_powerbi.csv"
SUMMARY_PATH = Path("data") / "opex_costcenter_summary.csv"


def main():
    try:
        # 1. Load data
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Input data file not found: {DATA_PATH}")
        
        print(f"Loading data from: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        
        if df.empty:
            raise ValueError("Input data file is empty.")
        
        print(f"Loaded {len(df)} rows of data.")

        # 2. Build model and calculate variances
        print("Building OPEX model and calculating variances...")
        model = OPEXModel(df)
        processed_df = model.get_processed_frame()
        summary_df = model.summarize_by_cost_center()

        # 3. Ensure output directory exists
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

        # 4. Save for Power BI or further analysis
        processed_df.to_csv(OUTPUT_PATH, index=False)
        summary_df.to_csv(SUMMARY_PATH, index=False)

        print(f"✓ Processed OPEX data saved to: {OUTPUT_PATH}")
        print(f"✓ Cost center summary saved to: {SUMMARY_PATH}")
        print("Variance analysis completed successfully.")
        
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
