"""
High-level pipeline:
1) Run variance analysis (Budget vs Actual, etc.)
2) Run forecast pipeline (run-rate + growth)
This simulates a monthly FP&A refresh process.
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    try:
        # Change to script directory to ensure relative paths work
        script_dir = Path(__file__).parent.parent
        original_dir = Path.cwd()
        
        try:
            os.chdir(script_dir)
            
            print("=" * 60)
            print("FP&A OPEX Dashboard - Full Pipeline")
            print("=" * 60)
            
            print("\nStep 1: Running variance analysis...")
            result = subprocess.run(
                ["python", "scripts/variance_analysis.py"],
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            
            print("\nStep 2: Running forecast pipeline...")
            result = subprocess.run(
                ["python", "scripts/forecast_pipeline.py"],
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            
            print("\n" + "=" * 60)
            print("✓ All steps completed successfully!")
            print("Data is ready for Power BI / analysis.")
            print("=" * 60)
            
        finally:
            os.chdir(original_dir)
            
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Pipeline step failed with exit code {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Output: {e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
