import pandas as pd


class ForecastModel:
    """
    Simple forecasting helpers for FP&A:
    - Run-rate forecast
    - Simple growth forecast
    """

    def __init__(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("DataFrame is empty. Cannot initialize ForecastModel.")
        self.df = df.copy()

    def add_run_rate_forecast(self, metric: str = "Actuals") -> pd.DataFrame:
        """
        Very simple run-rate forecast:
        - Take the latest month actual for each cost center
        - Annualize it for the remaining months.
        """
        if metric not in self.df.columns:
            raise ValueError(f"Column '{metric}' not found in dataframe.")
        
        if "Month" not in self.df.columns:
            raise ValueError("Column 'Month' not found. Cannot calculate run-rate forecast.")
        
        if "CostCenter" not in self.df.columns:
            raise ValueError("Column 'CostCenter' not found. Cannot calculate run-rate forecast.")
        
        df = self.df.copy()
        
        try:
            # Extract month number from Month column (assuming format YYYY-MM)
            df["Month_Num"] = pd.to_datetime(df["Month"], format="%Y-%m").dt.month
        except (ValueError, TypeError):
            # Fallback: try string slicing if datetime conversion fails
            df["Month_Num"] = df["Month"].astype(str).str.slice(5, 7).astype(int)

        latest_per_cc = (
            df.sort_values("Month_Num")
            .groupby("CostCenter")
            .tail(1)[["CostCenter", metric, "Month_Num"]]
            .rename(columns={metric: "Latest_Value"})
        )

        # Merge back
        df = df.merge(
            latest_per_cc[["CostCenter", "Latest_Value", "Month_Num"]],
            on=["CostCenter", "Month_Num"],
            how="left",
            suffixes=("", "_latest"),
        )

        # If Latest_Value is NaN after merge, fill with current metric value
        df["Latest_Value"] = df["Latest_Value"].fillna(df[metric])

        # Remaining months in year
        df["Remaining_Months"] = 12 - df["Month_Num"]
        df["Remaining_Months"] = df["Remaining_Months"].clip(lower=0)  # Ensure non-negative
        df["RunRateForecast_Annualized"] = df["Latest_Value"] * df["Remaining_Months"]

        self.df = df
        return self.df

    def add_simple_growth_forecast(self, growth_rate: float = 0.02) -> pd.DataFrame:
        """
        Apply a simple uniform growth rate to Actuals
        to create a next-period forecast.
        """
        if "Actuals" not in self.df.columns:
            raise ValueError("Column 'Actuals' not found. Cannot calculate growth forecast.")
        
        if not isinstance(growth_rate, (int, float)):
            raise ValueError(f"growth_rate must be a number, got {type(growth_rate)}")
        
        self.df["GrowthForecast"] = self.df["Actuals"] * (1 + growth_rate)
        return self.df
