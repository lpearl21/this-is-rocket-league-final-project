"""
Rocket League Player Earnings Scraper
Scrapes player earnings data from Liquipedia's Rocket League wiki
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_player_earnings():
    """
    Scrapes the top player earnings from Liquipedia Rocket League
    Returns a DataFrame with player stats
    """
    
    url = "https://liquipedia.net/rocketleague/Portal:Statistics/Player_earnings"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("Fetching data from Liquipedia...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main data table
    table = soup.find('table', class_='wikitable')
    
    if not table:
        print("Error: Could not find earnings table")
        return None
    
    # Lists to store data
    players = []
    countries = []
    first_place = []
    second_place = []
    third_place = []
    earnings = []
    
    # Find all rows (skip header)
    rows = table.find_all('tr')[1:]
    
    print(f"Found {len(rows)} player rows...")
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) >= 7:
            # Extract player name (cell 1)
            player_cell = cells[1]
            player_name = player_cell.get_text(strip=True)
            
            # Extract country from flag image
            flag_img = player_cell.find('img')
            if flag_img:
                # Country is usually in the alt text or parent link
                flag_link = player_cell.find('a')
                if flag_link and flag_link.get('title'):
                    country = flag_link.get('title')
                else:
                    country = "Unknown"
            else:
                country = "Unknown"
            
            # Extract placement stats (cells 3, 4, 5)
            try:
                first = int(cells[3].get_text(strip=True))
            except (ValueError, IndexError):
                first = 0
                
            try:
                second = int(cells[4].get_text(strip=True))
            except (ValueError, IndexError):
                second = 0
                
            try:
                third = int(cells[5].get_text(strip=True))
            except (ValueError, IndexError):
                third = 0
            
            # Extract earnings (last cell)
            earnings_text = cells[-1].get_text(strip=True)
            # Remove $ and commas, convert to float
            earnings_clean = earnings_text.replace('$', '').replace(',', '')
            try:
                earnings_val = float(earnings_clean)
            except ValueError:
                earnings_val = 0.0
            
            # Clean player name (remove country prefix if present)
            # The name often includes the country, so we need to clean it
            player_name_clean = player_name
            if country != "Unknown" and country in player_name:
                player_name_clean = player_name.replace(country, '').strip()
            
            players.append(player_name_clean)
            countries.append(country)
            first_place.append(first)
            second_place.append(second)
            third_place.append(third)
            earnings.append(earnings_val)
    
    # Create DataFrame
    df = pd.DataFrame({
        'player': players,
        'country': countries,
        'first_place': first_place,
        'second_place': second_place,
        'third_place': third_place,
        'earnings': earnings
    })
    
    print(f"Successfully scraped {len(df)} players!")
    
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


def main():
    # Scrape the data
    df = scrape_player_earnings()
    
    if df is not None:
        # Add region classification
        df['region'] = df['country'].apply(classify_region)
        
        # Add total wins column
        df['total_wins'] = df['first_place'] + df['second_place'] + df['third_place']
        
        # Add earnings per win (handle division by zero)
        df['earnings_per_win'] = df.apply(
            lambda x: x['earnings'] / x['total_wins'] if x['total_wins'] > 0 else 0, 
            axis=1
        )
        
        # Save to CSV
        output_path = '../data/rl_player_earnings.csv'
        df.to_csv(output_path, index=False)
        print(f"\nData saved to {output_path}")
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"Total players scraped: {len(df)}")
        print(f"\nPlayers by region:")
        print(df['region'].value_counts())
        print(f"\nTop 5 earners:")
        print(df[['player', 'country', 'earnings']].head())
        
    return df


if __name__ == "__main__":
    main()
