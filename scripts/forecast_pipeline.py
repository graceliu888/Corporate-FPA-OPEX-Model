"""
Script to:
1) Load already processed OPEX data
2) Generate simple run-rate & growth forecasts
3) Export result for visualization or further analysis
"""

import sys
import pandas as pd
from pathlib import Path
from models.forecast_model import ForecastModel

INPUT_PATH = Path("data") / "opex_processed_for_powerbi.csv"
OUTPUT_PATH = Path("data") / "opex_with_forecast.csv"


def main():
    try:
        # 1. Load data
        if not INPUT_PATH.exists():
            raise FileNotFoundError(
                f"Input data file not found: {INPUT_PATH}\n"
                "Please run variance_analysis.py first to generate the processed data."
            )
        
        print(f"Loading processed data from: {INPUT_PATH}")
        df = pd.read_csv(INPUT_PATH)
        
        if df.empty:
            raise ValueError("Input data file is empty.")
        
        print(f"Loaded {len(df)} rows of data.")

        # 2. Generate forecasts
        print("Generating forecasts...")
        forecast_model = ForecastModel(df)
        df = forecast_model.add_run_rate_forecast(metric="Actuals")
        df = forecast_model.add_simple_growth_forecast(growth_rate=0.03)

        # 3. Ensure output directory exists
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        # 4. Save results
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"✓ Forecasted OPEX data saved to: {OUTPUT_PATH}")
        print("Forecast pipeline completed successfully.")
        
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
