"""
Lab2.py  –  Exploratory Data Analysis: World Energy Dataset
============================================================
Chart types used (aligned with KQC7016 Week 4 & 5 lecture content):
  Fig 1  – Histogram          : Univariate distribution of primary energy consumption
  Fig 2  – Box Plot           : Univariate spread & outlier detection of energy per capita
  Fig 3  – Line Chart         : Time-series trend (fossil vs renewables, World aggregate)
  Fig 4  – Bar Chart          : Category comparison – energy mix by country (2022)
  Fig 5  – Pie Chart          : Proportional structure – global energy mix (2022)
  Fig 6  – Scatter Plot       : Bivariate relationship – GDP per capita vs GHG per capita
  Fig 7  – Heatmap            : Multivariate correlation matrix

Usage:
  1. Place this file in the SAME folder as WorldEnergy.csv
  2. Run:  python Lab2.py
  3. Each figure pops up on screen; close one window to see the next.

Required:  pip install pandas matplotlib seaborn
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

# ── Load data ─────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WorldEnergy.csv")
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("  WORLD ENERGY DATASET  –  EDA  (KQC7016 Lab 2)")
print("=" * 60)
print(f"  Rows      : {df.shape[0]:,}")
print(f"  Columns   : {df.shape[1]}")
print(f"  Year span : {int(df['year'].min())} – {int(df['year'].max())}")
print(f"  Entities  : {df['country'].nunique()}")
print("=" * 60, "\n")

# ── Filters ───────────────────────────────────────────────────────────────────
MAJOR = ["United States", "China", "India", "Germany",
         "United Kingdom", "Brazil", "Japan", "France"]

# Country-level only (drop regional / income aggregates)
df_countries = df[~df["country"].str.contains(
    r"\(|Africa|Asia|Europe|World|OECD|G20|income", na=False, regex=True)]

df_recent = df_countries[df_countries["year"] >= 2000].copy()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 1 – HISTOGRAM (Univariate Analysis)
# Purpose : Show the frequency distribution of primary energy consumption,
#           revealing the heavy right-skew caused by large economies.
# ══════════════════════════════════════════════════════════════════════════════
data_hist = df_recent["primary_energy_consumption"].dropna()
cap = data_hist.quantile(0.99)  # cap at 99th pct for readability
data_capped = data_hist[data_hist <= cap]

fig, ax = plt.subplots(figsize=(10, 5))

ax.hist(data_capped, bins=50, color="#2980b9", edgecolor="white",
        linewidth=0.5, alpha=0.85)

ax.axvline(data_capped.mean(), color="#e74c3c", linewidth=2,
           linestyle="--", label=f"Mean  : {data_capped.mean():.0f} TWh")
ax.axvline(data_capped.median(), color="#27ae60", linewidth=2,
           linestyle="-", label=f"Median: {data_capped.median():.0f} TWh")

ax.set_xlabel("Primary Energy Consumption (TWh)")
ax.set_ylabel("Number of Country-Year Records")
ax.set_title("Fig 1  –  Histogram: Distribution of Primary Energy Consumption\n"
             "(Country-level, 2000–2024; capped at 99th percentile for clarity)",
             fontweight="bold")
ax.legend(fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 2 – BOX PLOT (Univariate: Spread & Outlier Detection)
# Purpose : Compare energy-per-capita spread across major economies and
#           detect outliers — applying the "Detect Outliers" EDA step.
# ══════════════════════════════════════════════════════════════════════════════
bp_data = df_recent[df_recent["country"].isin(MAJOR)][
    ["country", "energy_per_capita"]].dropna()

order = (bp_data.groupby("country")["energy_per_capita"]
         .median().sort_values(ascending=False).index.tolist())

fig, ax = plt.subplots(figsize=(12, 5))

sns.boxplot(data=bp_data, x="country", y="energy_per_capita",
            order=order, palette="Set2", width=0.55,
            flierprops=dict(marker="o", markersize=4,
                            markerfacecolor="#e74c3c", alpha=0.6),
            ax=ax)

ax.set_xlabel("")
ax.set_ylabel("Energy per Capita (kWh per person)")
ax.set_title("Fig 2  –  Box Plot: Energy per Capita – Major Economies (2000–2024)\n"
             "Red dots = statistical outliers",
             fontweight="bold")
ax.set_xticklabels(order, rotation=25, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.grid(axis="y", alpha=0.4)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 3 – LINE CHART (Time-Series Trend)
# Purpose : Track the global shift from fossil fuels to renewables over
#           four decades — time-based pattern analysis.
# ══════════════════════════════════════════════════════════════════════════════
world = df[df["country"] == "World"][
    ["year", "fossil_share_energy", "renewables_share_energy",
     "solar_share_elec", "wind_share_elec"]].dropna(
    subset=["fossil_share_energy", "renewables_share_energy"])
world = world[world["year"] >= 1980].sort_values("year")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Fig 3  –  Line Chart: Global Energy Transition Trends (1980–2024)",
             fontweight="bold", fontsize=13)

# Left: fossil vs renewables share of primary energy
axes[0].plot(world["year"], world["fossil_share_energy"],
             color="#e74c3c", linewidth=2.5, label="Fossil Fuels")
axes[0].plot(world["year"], world["renewables_share_energy"],
             color="#27ae60", linewidth=2.5, label="Renewables")
axes[0].fill_between(world["year"], world["fossil_share_energy"],
                     alpha=0.08, color="#e74c3c")
axes[0].fill_between(world["year"], world["renewables_share_energy"],
                     alpha=0.15, color="#27ae60")
axes[0].set_xlabel("Year")
axes[0].set_ylabel("Share of Primary Energy (%)")
axes[0].set_title("Fossil Fuels vs. Renewables – Primary Energy Share")
axes[0].legend(fontsize=10)
axes[0].grid(alpha=0.35)

# Right: solar & wind share of electricity from 2000
sw = world[world["year"] >= 2000].dropna(
    subset=["solar_share_elec", "wind_share_elec"])
axes[1].plot(sw["year"], sw["solar_share_elec"],
             color="#f39c12", linewidth=2.5, marker="o",
             markersize=3, label="Solar")
axes[1].plot(sw["year"], sw["wind_share_elec"],
             color="#2980b9", linewidth=2.5, marker="s",
             markersize=3, label="Wind")
axes[1].set_xlabel("Year")
axes[1].set_ylabel("Share of Electricity (%)")
axes[1].set_title("Solar & Wind – Share of Electricity Generation")
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.35)

plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 4 – BAR CHART (Category Comparison)
# Purpose : Compare each major economy's energy source breakdown in 2022
#           using stacked bars — categorical comparison per lecture slides.
# ══════════════════════════════════════════════════════════════════════════════
energy_cols = ["coal_share_energy", "oil_share_energy", "gas_share_energy",
               "nuclear_share_energy", "renewables_share_energy"]
col_labels = ["Coal", "Oil", "Gas", "Nuclear", "Renewables"]
bar_colors = ["#2c3e50", "#8e44ad", "#e67e22", "#3498db", "#27ae60"]

mix_2022 = df_countries[
    (df_countries["year"] == 2022) &
    (df_countries["country"].isin(MAJOR))
    ][["country"] + energy_cols].set_index("country").dropna()

fig, ax = plt.subplots(figsize=(13, 5))

mix_2022[energy_cols].plot(kind="bar", stacked=True,
                           color=bar_colors, ax=ax,
                           width=0.65, edgecolor="white", linewidth=0.4)

ax.set_ylabel("Share of Primary Energy (%)")
ax.set_xlabel("")
ax.set_title("Fig 4  –  Bar Chart: Energy Mix by Source – Major Economies (2022)\n"
             "Stacked bars show each country's proportional fuel breakdown",
             fontweight="bold")
ax.legend(col_labels, loc="upper right", fontsize=9,
          title="Energy Source", title_fontsize=9)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
ax.grid(axis="y", alpha=0.35)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 5 – PIE CHART (Proportional Structure)
# Purpose : Show global primary energy proportions clearly for a general
#           audience — proportional structure view per lecture slides.
# ══════════════════════════════════════════════════════════════════════════════
world_pie = df[df["country"] == "World"][
    ["year"] + energy_cols].dropna().sort_values("year")

# Use 2022 if available, otherwise latest year
target_yr = 2022 if 2022 in world_pie["year"].values else world_pie["year"].max()
pie_row = world_pie[world_pie["year"] == target_yr]
pie_vals = pie_row[energy_cols].values.flatten()

fig, ax = plt.subplots(figsize=(9, 7))

wedges, texts, autotexts = ax.pie(
    pie_vals,
    labels=col_labels,
    colors=bar_colors,
    explode=[0.03] * len(pie_vals),
    autopct=lambda p: f"{p:.1f}%" if p > 2 else "",
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=1.5)
)

for text in texts:
    text.set_fontsize(11)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax.set_title(f"Fig 5  –  Pie Chart: Global Primary Energy Mix (World, {target_yr})\n"
             "Proportional share of each energy source",
             fontweight="bold", pad=20)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 6 – SCATTER PLOT (Bivariate Relationship)
# Purpose : Explore the relationship between GDP per capita and GHG
#           emissions per capita — bivariate numerical analysis.
# ══════════════════════════════════════════════════════════════════════════════
yr2022 = df_countries[df_countries["year"] == 2022][
    ["country", "gdp", "greenhouse_gas_emissions",
     "population", "renewables_share_energy"]
].dropna().copy()

yr2022["ghg_per_capita"] = (yr2022["greenhouse_gas_emissions"]
                            / yr2022["population"] * 1e6)
yr2022["gdp_per_capita"] = yr2022["gdp"] / yr2022["population"]

fig, ax = plt.subplots(figsize=(11, 6))

sc = ax.scatter(
    yr2022["gdp_per_capita"] / 1000,
    yr2022["ghg_per_capita"],
    c=yr2022["renewables_share_energy"],
    cmap="RdYlGn", s=70, alpha=0.78,
    edgecolors="grey", linewidths=0.4
)

cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Renewables Share of Energy (%)", fontsize=10)

for _, row in yr2022[yr2022["country"].isin(MAJOR)].iterrows():
    ax.annotate(
        row["country"],
        (row["gdp_per_capita"] / 1000, row["ghg_per_capita"]),
        fontsize=8, ha="left", va="bottom",
        xytext=(5, 3), textcoords="offset points",
        arrowprops=dict(arrowstyle="-", color="grey", lw=0.6)
    )

ax.set_xlabel("GDP per Capita (USD thousands)")
ax.set_ylabel("GHG Emissions per Capita (t CO2eq)")
ax.set_title("Fig 6  –  Scatter Plot: GDP per Capita vs. GHG Emissions per Capita (2022)\n"
             "Colour = Renewable Energy Share  |  Labelled: major economies",
             fontweight="bold")
ax.grid(alpha=0.35)
plt.tight_layout()
plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# Figure 7 – HEATMAP (Multivariate Correlation)
# Purpose : Reveal pairwise Pearson correlations among key energy variables
#           — multivariate analysis, heatmap for finding correlation.
# ══════════════════════════════════════════════════════════════════════════════
corr_cols = [
    "fossil_share_energy",
    "renewables_share_energy",
    "solar_share_energy",
    "wind_share_energy",
    "coal_share_energy",
    "nuclear_share_energy",
    "greenhouse_gas_emissions",
    "gdp",
    "primary_energy_consumption",
]
corr_labels = [
    "Fossil Share",
    "Renewables Share",
    "Solar Share",
    "Wind Share",
    "Coal Share",
    "Nuclear Share",
    "GHG Emissions",
    "GDP",
    "Primary Energy",
]

corr_df = df_recent[corr_cols].dropna()
corr_matrix = corr_df.corr()
corr_matrix.index = corr_labels
corr_matrix.columns = corr_labels

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    vmin=-1, vmax=1,
    ax=ax,
    linewidths=0.5,
    annot_kws={"size": 9},
    square=True
)

ax.set_title("Fig 7  –  Heatmap: Pearson Correlation Matrix – Key Energy Variables\n"
             "(Country-level records, 2000–2024)",
             fontweight="bold", pad=14)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=9)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
plt.tight_layout()
plt.show()

# ── Summary ───────────────────────────────────────────────────────────────────
print("\nEDA complete.  All 7 figures displayed.")
print("\nChart type summary (KQC7016 aligned):")
print("  Fig 1 – Histogram    : Univariate distribution")
print("  Fig 2 – Box Plot     : Spread & outlier detection")
print("  Fig 3 – Line Chart   : Time-series trend")
print("  Fig 4 – Bar Chart    : Category comparison")
print("  Fig 5 – Pie Chart    : Proportional structure")
print("  Fig 6 – Scatter Plot : Bivariate relationship")
print("  Fig 7 – Heatmap      : Multivariate correlation")
