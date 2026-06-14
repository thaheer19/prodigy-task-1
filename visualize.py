import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. READ DATA: Skip the first 4 metadata rows built into World Bank CSVs
csv_name = "API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv" # Confirm your actual filename matches this

if not os.path.exists(csv_name):
    print(f"Error: Could not find '{csv_name}' in this folder. Make sure names match exactly!")
else:
    df = pd.read_csv(csv_name, skiprows=4)
    df.columns = df.columns.str.strip() # Clean formatting spaces

    # Pick the most recent available data year column automatically
    year_columns = [col for col in df.columns if col.isdigit()]
    latest_year = year_columns[-1]
    print(f"Dataset loaded! Processing data distributions for the year: {latest_year}")

    # Drop entries missing data for our target year
    df_clean = df.dropna(subset=[latest_year])

    # -----------------------------------------------------------------
    # VISUALIZATION 1: BAR CHART (Categorical/Group Distribution)
    # -----------------------------------------------------------------
    # We take the top 15 areas by population to keep the chart readable
    top_15 = df_clean.sort_values(by=latest_year, ascending=False).head(15)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=latest_year, y='Country Name', data=top_15, hue='Country Name', palette='plasma', legend=False)
    plt.title(f'Top 15 Most Populous Countries/Regions ({latest_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Total Population Size', fontsize=12)
    plt.ylabel('Country Name / Aggregate Region', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('population_bar_chart.png', dpi=300) # Saves directly to your folder
    plt.show()

    # -----------------------------------------------------------------
    # VISUALIZATION 2: HISTOGRAM (Continuous Data Distribution)
    # -----------------------------------------------------------------
    # Filter out massive regional aggregates (like 'World') to see real country distributions
    countries_only = df_clean[df_clean[latest_year] < 400_000_000]

    plt.figure(figsize=(10, 6))
    sns.histplot(data=countries_only, x=latest_year, bins=25, kde=True, color='darkcyan')
    plt.title(f'Distribution of Global Country Populations ({latest_year})', fontsize=14, fontweight='bold')
    plt.xlabel('Population Groups', fontsize=12)
    plt.ylabel('Number of Countries', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('population_histogram.png', dpi=300) # Saves directly to your folder
    plt.show()
    print("Done! Check your folder for 'population_bar_chart.png' and 'population_histogram.png'.")
