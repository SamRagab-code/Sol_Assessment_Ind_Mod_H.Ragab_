import datetime as dt
import pandas as pd
import numpy as np

class IndexModel:
    def __init__(self) -> None:
        """Initialize the index model."""
        self.price_data = price_data.copy()
        self.price_data.index = pd.to_datetime(self.price_data.index)
        self.index_series = pd.Series(dtype="float64")

    def calc_index_level(self, start_date: dt.date, end_date: dt.date,  base_value: float = 100.0) -> pd.Series:
        """Calculate index levels."""
        # Slice date range
        price_data = self.price_data.loc[(self.price_data.index.date >= start_date) & 
                                         (self.price_data.index.date <= end_date)]
        
        # Compute daily returns
        daily_returns = price_data.pct_change()

        # Identify month boundaries
        group_firstdays = price_data.groupby([price_data.index.year, price_data.index.month]).apply(lambda x: x.index[0])
        group_lastdays = price_data.groupby([price_data.index.year, price_data.index.month]).apply(lambda x: x.index[-1])

        # Determine top 3 stocks at the beginning of each month
        month_start_prices = price_data.loc[group_firstdays]
        top_3_constituents = month_start_prices.apply(lambda row: row.nlargest(3).index.tolist(), axis=1)

        # Prepare index series
        index_series = pd.Series(index=price_data.index, dtype="float64")
        index_value = base_value
        first_valid_date = price_data.index[0]
        index_series.loc[first_valid_date] = index_value

        for i, start_date in enumerate(group_firstdays):
            if i >= len(group_lastdays):
                break
            end_date = group_lastdays.iloc[i]

            top_stocks = top_3_constituents.loc[start_date]
            weights = pd.Series([0.5, 0.25, 0.25], index=top_stocks)

            # Daily returns of selected constituents
            period_returns = daily_returns.loc[start_date:end_date, top_stocks]

            for date, row in period_returns.iterrows():
                try:
                    weighted_return = (1 + row).pow(weights).prod() - 1
                    index_value *= (1 + weighted_return)
                    index_series.loc[date] = index_value
                except Exception as e:
                    print(f"Error on {date.date()}: {e}")

        self.index_series = index_series.ffill().dropna()
        return self.index_series

    def export_values(self, file_name: str) -> None:
        """Export calculated index levels to CSV."""
        if self.index_series.empty:
            print("No index values to export. Please run `calc_index_level` first.")
        else:
            self.index_series.to_csv(file_name, header=["Index_Level"])
            print(f"Index levels successfully exported to {file_name}")

    def plot_index(self) -> None:
        """Plot the index levels."""
        if self.index_series.empty:
            print("No index values to plot. Please run `calc_index_level` first.")
        else:
            plt.figure(figsize=(12, 6))
            plt.plot(self.index_series, label="Custom Index", color='blue')
            plt.title("Custom Weighted Index Level")
            plt.xlabel("Date")
            plt.ylabel("Index Level")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
