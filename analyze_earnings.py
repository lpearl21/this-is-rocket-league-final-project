"""
Rocket League Earnings Analysis
Analyzes regional differences and correlation between wins and earnings
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def load_data(filepath='../data/rl_player_earnings.csv'):
    """Load the scraped data and add derived columns"""
    df = pd.read_csv(filepath)
    
    # Add region classification
    df['region'] = df['country'].apply(classify_region)
    
    # Add total wins column
    df['total_wins'] = df['first_place'] + df['second_place'] + df['third_place']
    
    # Add earnings per win (handle division by zero)
    df['earnings_per_win'] = df.apply(
        lambda x: x['earnings'] / x['total_wins'] if x['total_wins'] > 0 else 0, 
        axis=1
    )
    
    return df


def classify_region(country):
    """
    Classifies a country into NA, EU, or Other region
    """
    na_countries = [
        'United States', 'Canada', 'Mexico'
    ]
    
    eu_countries = [
        'France', 'England', 'Germany', 'Spain', 'Netherlands', 
        'Sweden', 'Belgium', 'Denmark', 'Finland', 'Norway',
        'Austria', 'Italy', 'Poland', 'Scotland', 'Wales',
        'Ireland', 'Northern Ireland', 'Portugal', 'Iceland',
        'Lithuania', 'Switzerland', 'United Kingdom'
    ]
    
    if country in na_countries:
        return 'NA'
    elif country in eu_countries:
        return 'EU'
    else:
        return 'Other'


def regional_comparison(df):
    """
    Compare earnings between NA and EU regions
    """
    print("\n" + "="*60)
    print("REGIONAL COMPARISON: NA vs EU")
    print("="*60)
    
    # Filter to just NA and EU
    na_eu = df[df['region'].isin(['NA', 'EU'])]
    
    # Group by region
    regional_stats = na_eu.groupby('region').agg({
        'earnings': ['sum', 'mean', 'median', 'count'],
        'first_place': 'sum',
        'total_wins': 'sum',
        'earnings_per_win': 'mean'
    }).round(2)
    
    print("\nRegional Statistics:")
    print(regional_stats)
    
    # Calculate specific comparisons
    na_data = df[df['region'] == 'NA']
    eu_data = df[df['region'] == 'EU']
    
    print(f"\n--- Summary ---")
    print(f"NA Players: {len(na_data)}")
    print(f"EU Players: {len(eu_data)}")
    print(f"\nNA Total Earnings: ${na_data['earnings'].sum():,.2f}")
    print(f"EU Total Earnings: ${eu_data['earnings'].sum():,.2f}")
    print(f"\nNA Average Earnings: ${na_data['earnings'].mean():,.2f}")
    print(f"EU Average Earnings: ${eu_data['earnings'].mean():,.2f}")
    print(f"\nNA Avg Earnings Per Win: ${na_data['earnings_per_win'].mean():,.2f}")
    print(f"EU Avg Earnings Per Win: ${eu_data['earnings_per_win'].mean():,.2f}")
    
    return regional_stats


def correlation_analysis(df):
    """
    Analyze correlation between tournament wins and earnings
    """
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS: Wins vs Earnings")
    print("="*60)
    
    # Overall correlation
    corr_total, p_total = stats.pearsonr(df['total_wins'], df['earnings'])
    corr_first, p_first = stats.pearsonr(df['first_place'], df['earnings'])
    
    print(f"\nTotal Wins vs Earnings:")
    print(f"  Correlation (r): {corr_total:.4f}")
    print(f"  P-value: {p_total:.4e}")
    print(f"  Interpretation: {'Strong' if abs(corr_total) > 0.7 else 'Moderate' if abs(corr_total) > 0.4 else 'Weak'} positive correlation")
    
    print(f"\n1st Place Finishes vs Earnings:")
    print(f"  Correlation (r): {corr_first:.4f}")
    print(f"  P-value: {p_first:.4e}")
    
    # Correlation by region
    print("\n--- Correlation by Region ---")
    for region in ['NA', 'EU']:
        region_df = df[df['region'] == region]
        if len(region_df) > 2:
            r, p = stats.pearsonr(region_df['total_wins'], region_df['earnings'])
            print(f"{region}: r = {r:.4f} (p = {p:.4e})")
    
    return corr_total, corr_first


def efficiency_analysis(df):
    """
    Analyze which region is more 'efficient' (earnings per win)
    """
    print("\n" + "="*60)
    print("EFFICIENCY ANALYSIS: Earnings Per Win by Region")
    print("="*60)
    
    # Filter out players with 0 wins to avoid skewing
    df_winners = df[df['total_wins'] > 0]
    
    na_eff = df_winners[df_winners['region'] == 'NA']['earnings_per_win']
    eu_eff = df_winners[df_winners['region'] == 'EU']['earnings_per_win']
    
    print(f"\nNA Earnings Per Win:")
    print(f"  Mean: ${na_eff.mean():,.2f}")
    print(f"  Median: ${na_eff.median():,.2f}")
    print(f"  Players with wins: {len(na_eff)}")
    
    print(f"\nEU Earnings Per Win:")
    print(f"  Mean: ${eu_eff.mean():,.2f}")
    print(f"  Median: ${eu_eff.median():,.2f}")
    print(f"  Players with wins: {len(eu_eff)}")
    
    # Statistical test
    if len(na_eff) > 2 and len(eu_eff) > 2:
        t_stat, p_val = stats.ttest_ind(na_eff, eu_eff)
        print(f"\nT-test (NA vs EU efficiency):")
        print(f"  t-statistic: {t_stat:.4f}")
        print(f"  p-value: {p_val:.4f}")
        if p_val < 0.05:
            winner = "NA" if na_eff.mean() > eu_eff.mean() else "EU"
            print(f"  Result: {winner} is significantly more efficient!")
        else:
            print(f"  Result: No significant difference in efficiency")
    
    return na_eff.mean(), eu_eff.mean()


def create_visualizations(df, output_dir='../data/'):
    """
    Create visualizations for the analysis
    """
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Figure 1: Regional Earnings Comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Bar chart of total earnings by region
    na_eu = df[df['region'].isin(['NA', 'EU'])]
    regional_totals = na_eu.groupby('region')['earnings'].sum() / 1_000_000
    
    ax1 = axes[0]
    bars = ax1.bar(regional_totals.index, regional_totals.values, color=['#1f77b4', '#ff7f0e'])
    ax1.set_ylabel('Total Earnings (Millions $)')
    ax1.set_title('Total Prize Money: NA vs EU')
    ax1.bar_label(bars, fmt='$%.2fM')
    
    # Bar chart of average earnings
    regional_avg = na_eu.groupby('region')['earnings'].mean() / 1000
    ax2 = axes[1]
    bars2 = ax2.bar(regional_avg.index, regional_avg.values, color=['#1f77b4', '#ff7f0e'])
    ax2.set_ylabel('Average Earnings (Thousands $)')
    ax2.set_title('Average Earnings Per Player: NA vs EU')
    ax2.bar_label(bars2, fmt='$%.0fK')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}regional_comparison.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {output_dir}regional_comparison.png")
    plt.close()
    
    # Figure 2: Correlation Scatterplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = {'NA': '#1f77b4', 'EU': '#ff7f0e', 'Other': '#2ca02c'}
    
    for region in ['NA', 'EU', 'Other']:
        region_df = df[df['region'] == region]
        ax.scatter(region_df['total_wins'], region_df['earnings'] / 1000, 
                   label=region, alpha=0.6, c=colors[region], s=50)
    
    # Add trend line
    z = np.polyfit(df['total_wins'], df['earnings'] / 1000, 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['total_wins'].min(), df['total_wins'].max(), 100)
    ax.plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend Line')
    
    ax.set_xlabel('Total Tournament Placements (1st + 2nd + 3rd)')
    ax.set_ylabel('Total Earnings (Thousands $)')
    ax.set_title('Tournament Success vs Earnings')
    ax.legend()
    
    # Add correlation annotation
    corr, _ = stats.pearsonr(df['total_wins'], df['earnings'])
    ax.annotate(f'r = {corr:.3f}', xy=(0.05, 0.95), xycoords='axes fraction',
                fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}correlation_plot.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {output_dir}correlation_plot.png")
    plt.close()
    
    # Figure 3: Efficiency Comparison
    fig, ax = plt.subplots(figsize=(8, 5))
    
    df_winners = df[(df['total_wins'] > 0) & (df['region'].isin(['NA', 'EU']))]
    
    efficiency_data = [
        df_winners[df_winners['region'] == 'NA']['earnings_per_win'] / 1000,
        df_winners[df_winners['region'] == 'EU']['earnings_per_win'] / 1000
    ]
    
    bp = ax.boxplot(efficiency_data, labels=['NA', 'EU'], patch_artist=True)
    bp['boxes'][0].set_facecolor('#1f77b4')
    bp['boxes'][1].set_facecolor('#ff7f0e')
    
    ax.set_ylabel('Earnings Per Win (Thousands $)')
    ax.set_title('Efficiency: Earnings Per Tournament Placement')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}efficiency_boxplot.png', dpi=150, bbox_inches='tight')
    print(f"Saved: {output_dir}efficiency_boxplot.png")
    plt.close()
    
    print("\nAll visualizations created!")


def main():
    # Load data
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} players")
    
    # Run analyses
    regional_comparison(df)
    correlation_analysis(df)
    efficiency_analysis(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
