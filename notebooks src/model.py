import numpy as np
import pandas as pd

class PolicySimulator:
    def __init__(
        self,
        years=10,
        simulations=10000,
        base_revenue=20,
        base_cost=32,
        revenue_sd=0.05,
        cost_sd=0.04,
        multiplier_mean=0.30,
        multiplier_sd=0.10
    ):
        self.years = years
        self.simulations = simulations
        self.base_revenue = base_revenue
        self.base_cost = base_cost
        self.revenue_sd = revenue_sd
        self.cost_sd = cost_sd
        self.multiplier_mean = multiplier_mean
        self.multiplier_sd = multiplier_sd

    def run_simulation(self):
        """Run all simulations and return yearly & cumulative results as DataFrames."""

        rng = np.random.default_rng()

        yearly_nets = np.zeros((self.simulations, self.years))

        for s in range(self.simulations):

            revenue = self.base_revenue
            cost = self.base_cost

            for y in range(self.years):
                
                revenue_growth = rng.normal(loc=0, scale=self.revenue_sd)
                cost_growth = rng.normal(loc=0, scale=self.cost_sd)
                multiplier_effect = rng.normal(
                    loc=self.multiplier_mean,
                    scale=self.multiplier_sd
                )

                revenue *= (1 + revenue_growth)
                cost *= (1 + cost_growth)
                net = revenue - cost + multiplier_effect

                yearly_nets[s, y] = net

        df_yearly = pd.DataFrame(yearly_nets)
        df_yearly.columns = [f"Year_{i+1}" for i in range(self.years)]

        df_cumulative = df_yearly.sum(axis=1)
        df_cumulative = pd.DataFrame({"Cumulative_10Y_Net": df_cumulative})

        return df_yearly, df_cumulative

    def summarize_yearly(self, df_yearly):
        """Return mean, median, p5, p95 for each year."""
        summary = {
            "year": [],
            "mean": [],
            "median": [],
            "p5": [],
            "p95": []
        }

        for i in range(self.years):
            col = df_yearly.iloc[:, i]
            summary["year"].append(i + 1)
            summary["mean"].append(col.mean())
            summary["median"].append(col.median())
            summary["p5"].append(col.quantile(0.05))
            summary["p95"].append(col.quantile(0.95))

        return pd.DataFrame(summary)

