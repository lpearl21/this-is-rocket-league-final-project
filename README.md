# Rocket League Esports: Money, Wins, and Regional Efficiency

A data analysis project examining prize money distribution and tournament success in professional Rocket League esports, with a focus on comparing North American (NA) and European (EU) players.

## Project Overview

This project scrapes player earnings data from [Liquipedia's Rocket League Wiki](https://liquipedia.net/rocketleague/Portal:Statistics/Player_earnings) and analyzes:

1. **Regional Comparison**: Which region (NA vs EU) has earned more total prize money?
2. **Correlation Analysis**: How strongly do tournament wins predict earnings?
3. **Efficiency Analysis**: Which region earns more money per tournament placement?

## Research Questions

- **Q1**: Do NA or EU players dominate Rocket League prize earnings?
- **Q2**: Is there a strong correlation between tournament placements and total earnings?
- **Q3**: Which region is more "efficient" — earning more per win?

## Repository Structure

```
rl_earnings_project/
├── data/
│   ├── rl_player_earnings.csv      # Scraped player data
│   ├── regional_comparison.png     # Visualization
│   ├── correlation_plot.png        # Visualization
│   └── efficiency_boxplot.png      # Visualization
├── scraping_code/
│   ├── scrape_earnings.py          # Web scraping script
│   └── analyze_earnings.py         # Analysis script
├── README.md
├── README.qmd
└── requirements.txt
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Scrape the Data

```bash
cd scraping_code
python scrape_earnings.py
```

This will:
- Fetch player earnings from Liquipedia
- Extract player names, countries, placements (1st/2nd/3rd), and earnings
- Classify players by region (NA, EU, Other)
- Save results to `data/rl_player_earnings.csv`

### Step 2: Run the Analysis

```bash
python analyze_earnings.py
```

This will:
- Calculate regional comparisons
- Compute correlation between wins and earnings
- Analyze efficiency (earnings per win)
- Generate visualizations

## Data Description

| Column | Description |
|--------|-------------|
| `player` | Player's gamertag |
| `country` | Player's country |
| `first_place` | Number of 1st place finishes |
| `second_place` | Number of 2nd place finishes |
| `third_place` | Number of 3rd place finishes |
| `earnings` | Total career prize earnings (USD) |
| `region` | Classified region (NA, EU, or Other) |
| `total_wins` | Sum of all placements |
| `earnings_per_win` | Earnings divided by total placements |

## Key Findings

*Run the analysis to populate these findings with your scraped data!*

- **Regional Dominance**: [EU/NA] players have earned more total prize money
- **Correlation**: Tournament success shows a [strong/moderate/weak] correlation with earnings (r = X.XX)
- **Efficiency**: [EU/NA] players earn more per tournament placement on average

## Visualizations

The analysis generates three visualizations:

1. **Regional Comparison Bar Chart**: Total and average earnings by region
2. **Correlation Scatterplot**: Tournament placements vs earnings with trend line
3. **Efficiency Boxplot**: Distribution of earnings-per-win by region

## Data Source

Data scraped from [Liquipedia Rocket League Wiki](https://liquipedia.net/rocketleague/Portal:Statistics/Player_earnings)

*Note: Please scrape responsibly and respect Liquipedia's terms of service.*

## Author

Liam Pearl - Unstructured Data Analysis Final Project

## License

This project is for educational purposes only.
