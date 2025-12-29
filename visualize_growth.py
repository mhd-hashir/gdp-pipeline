import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_gdp():
    csv_file = "gdp_history_2021_2025.csv"
    if not os.path.exists(csv_file):
        print(f"File {csv_file} not found.")
        return

    # Load data
    df = pd.read_csv(csv_file)
    
    # Filter top 10 countries by 2025 GDP for clearer plots
    top_10 = df.nlargest(10, '2025').copy()
    
    # Melt for Trend Line Plot
    # We want columns Country, Year, GDP
    df_melted = top_10.melt(id_vars=['Country'], 
                            value_vars=['2021', '2022', '2023', '2024', '2025'],
                            var_name='Year', value_name='GDP')
    
    # 1. Line Chart: GDP Trend (2021-2025)
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_melted, x='Year', y='GDP', hue='Country', marker='o')
    plt.title('GDP Trend for Top 10 Economies (2021-2025)')
    plt.ylabel('GDP (Million USD)')
    plt.xlabel('Year')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('gdp_trend_top10.png')
    print("Saved gdp_trend_top10.png")
    
    # 2. Bar Chart: Growth Rate (2024-2025)
    # Calculate growth %
    top_10['Growth_pct'] = ((top_10['2025'] - top_10['2024']) / top_10['2024']) * 100
    top_10 = top_10.sort_values(by='Growth_pct', ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10, x='Growth_pct', y='Country', hue='Country', palette='viridis', legend=False)
    plt.title('Projected GDP Growth Rate (2024-2025) for Top 10 Economies')
    plt.xlabel('Growth Rate (%)')
    plt.ylabel('Country')
    plt.axvline(x=0, color='black', linestyle='-')
    plt.tight_layout()
    plt.savefig('gdp_growth_rate_top10.png')
    print("Saved gdp_growth_rate_top10.png")
    
    plt.show()

if __name__ == "__main__":
    visualize_gdp()
