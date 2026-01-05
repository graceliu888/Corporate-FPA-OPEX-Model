import pandas as pd


class OPEXModel:
    """
    Core OPEX model for cost centers.
    - Calculates total OPEX
    - Calculates variances
    - Summarizes by cost center
    """

    REQUIRED_COLUMNS = ["Travel", "Software", "VendorSpend", "OfficeExpense"]
    REQUIRED_VARIANCE_COLUMNS = ["Budget", "Forecast", "Actuals"]

    def __init__(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("DataFrame is empty. Cannot initialize OPEXModel.")
        # Work on a copy to avoid mutating original
        self.df = df.copy()
        self._validate_columns()

    def _validate_columns(self) -> None:
        """Validate that required columns exist in the dataframe."""
        missing_cols = [col for col in self.REQUIRED_COLUMNS + self.REQUIRED_VARIANCE_COLUMNS 
                       if col not in self.df.columns]
        if missing_cols:
            raise ValueError(
                f"Missing required columns: {missing_cols}. "
                f"Available columns: {list(self.df.columns)}"
            )

    @classmethod
    def from_csv(cls, path: str) -> "OPEXModel":
        """Create an OPEXModel from a CSV file."""
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {path}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file {path}: {str(e)}")
        return cls(df)

    def calculate_total_opex(self) -> pd.DataFrame:
        """Add a Total_OPEX column based on key cost categories."""
        for col in self.REQUIRED_COLUMNS:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found. Cannot calculate Total_OPEX.")
        
        self.df["Total_OPEX"] = (
            self.df["Travel"]
            + self.df["Software"]
            + self.df["VendorSpend"]
            + self.df["OfficeExpense"]
        )
        return self.df

    def calculate_variances(self) -> pd.DataFrame:
        """Add variance columns: Budget vs Actual, etc."""
        for col in self.REQUIRED_VARIANCE_COLUMNS:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found. Cannot calculate variances.")
        
        self.df["Budget_vs_Actual"] = self.df["Actuals"] - self.df["Budget"]
        self.df["Forecast_vs_Actual"] = self.df["Actuals"] - self.df["Forecast"]
        self.df["Budget_vs_Forecast"] = self.df["Forecast"] - self.df["Budget"]
        return self.df

    def summarize_by_cost_center(self) -> pd.DataFrame:
        """
        Aggregate P&L-style view per cost center.
        Useful as a table for Power BI dashboards.
        Note: Requires variance columns to be calculated first.
        """
        if "CostCenter" not in self.df.columns:
            raise ValueError("Column 'CostCenter' not found. Cannot summarize by cost center.")
        
        # Check if variance columns exist, if not calculate them
        variance_cols = ["Budget_vs_Actual", "Forecast_vs_Actual", "Budget_vs_Forecast"]
        missing_variance_cols = [col for col in variance_cols if col not in self.df.columns]
        
        if missing_variance_cols:
            # Auto-calculate if missing
            self.calculate_variances()
        
        summary_cols = ["Budget", "Forecast", "Actuals"] + variance_cols
        available_cols = [col for col in summary_cols if col in self.df.columns]
        
        summary = (
            self.df.groupby("CostCenter")[available_cols]
            .sum()
            .reset_index()
        )
        return summary

    def get_processed_frame(self) -> pd.DataFrame:
        """
        Run full pipeline: total opex + variances.
        """
        self.calculate_total_opex()
        self.calculate_variances()
        return self.df
