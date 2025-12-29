import pandas as pd
import requests
import io
import re

def clean_value(val):
    if pd.isna(val):
        return None
    # Remove citations like [1], [n 1]
    val = re.sub(r'\[.*?\]', '', str(val))
    # Remove commas
    val = val.replace(',', '')
    # Check if number
    try:
        return float(val)
    except ValueError:
        return None

def clean_country(name):
    if pd.isna(name):
        return None
    # Remove citations and extra spaces
    name = re.sub(r'\[.*?\]', '', str(name))
    return name.strip()

def fetch_live_data():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    print(f"Fetching live data from {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = pd.read_html(io.StringIO(response.text))
    except Exception as e:
        print(f"Error fetching live data: {e}")
        raise

    target_table = None
    for df in tables:
        cols = [str(c) for c in df.columns]
        # Look for "Country" and "IMF"
        if any("Country" in c for c in cols) and any("IMF" in c for c in cols):
            target_table = df
            break
            
    if target_table is None:
        # Debugging: print first few tables' columns
        if tables:
            print("Could not find table. First table columns:", tables[0].columns)
        raise ValueError("Could not find Live GDP table in fetched content")
    
    # Flatten multi-index
    if isinstance(target_table.columns, pd.MultiIndex):
        target_table.columns = [' '.join(map(str, col)).strip() for col in target_table.columns.values]
    
    col_country = None
    col_2025 = None
    col_2024 = None
    
    for col in target_table.columns:
        if "Country" in col or "Territory" in col:
            col_country = col
        if "2025" in col and "IMF" in col:
            col_2025 = col
        if "2024" in col and "World Bank" in col:
            col_2024 = col
            
    # Try looser matching if exact failed
    if not all([col_country, col_2025, col_2024]):
        for col in target_table.columns:
            if ("Country" in col or "Territory" in col) and col_country is None: col_country = col
            if "2025" in col and col_2025 is None: col_2025 = col
            if "2024" in col and col_2024 is None: col_2024 = col

    print(f"Live Columns - Country: {col_country}, 2025: {col_2025}, 2024: {col_2024}")
    
    if not all([col_country, col_2025, col_2024]):
         raise ValueError(f"Could not identify all required columns. Found: {col_country}, {2024}, {col_2025}")

    df_extracted = target_table[[col_country, col_2024, col_2025]].copy()
    df_extracted.columns = ['Country', '2024', '2025']
    
    return df_extracted

def fetch_archived_data():
    url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    print(f"Fetching archived data from {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    tables = pd.read_html(io.StringIO(response.text))
    
    target_table = None
    for df in tables:
        cols = [str(c) for c in df.columns]
        if any("Country" in c for c in cols) and any("IMF" in c for c in cols):
             target_table = df
             break
             
    if target_table is None:
        raise ValueError("Could not find Archived GDP table")

    if isinstance(target_table.columns, pd.MultiIndex):
        target_table.columns = [' '.join(map(str, col)).strip() for col in target_table.columns.values]

    col_country = None
    col_2023 = None
    col_2022 = None
    col_2021 = None
    
    print("Available Archive Columns:", target_table.columns.tolist())

    for col in target_table.columns:
        if "Country" in col or "Territory" in col:
            col_country = col
        # IMF -> 2023
        if "IMF" in col and "Estimate" in col:
            col_2023 = col
        # WB -> 2022
        if "World Bank" in col and "Estimate" in col:
            col_2022 = col
        # UN -> 2021
        if "United Nations" in col and "Estimate" in col:
            col_2021 = col
            
    print(f"Archive Columns - Country: {col_country}, 2023: {col_2023}, 2022: {col_2022}, 2021: {col_2021}")
    
    # Check if we found them
    if not all([col_country, col_2023, col_2022, col_2021]):
         print("Warning: Missing some archive columns.")
    
    # Extract available
    extract_cols = [col_country]
    rename_map = {col_country: 'Country'}
    
    if col_2021: 
        extract_cols.append(col_2021)
        rename_map[col_2021] = '2021'
    if col_2022: 
        extract_cols.append(col_2022)
        rename_map[col_2022] = '2022'
    if col_2023: 
        extract_cols.append(col_2023)
        rename_map[col_2023] = '2023'
        
    df_extracted = target_table[extract_cols].copy()
    df_extracted = df_extracted.rename(columns=rename_map)
    
    return df_extracted

def main():
    # 1. Fetch
    df_live = fetch_live_data()
    df_archive = fetch_archived_data()
    
    # 2. Clean 'Country' for merging
    df_live['Country'] = df_live['Country'].apply(clean_country)
    df_archive['Country'] = df_archive['Country'].apply(clean_country)
    
    # 3. Clean numeric data
    for yr in ['2024', '2025']:
        df_live[yr] = df_live[yr].apply(clean_value)
        
    for yr in ['2021', '2022', '2023']:
        df_archive[yr] = df_archive[yr].apply(clean_value)
        
    # 4. Merge
    # Outer join to include all countries
    df_merged = pd.merge(df_archive, df_live, on='Country', how='outer')
    
    # Sort columns
    df_merged = df_merged[['Country', '2021', '2022', '2023', '2024', '2025']]
    
    # Sort by 2025 GDP desc
    df_merged = df_merged.sort_values(by='2025', ascending=False)
    
    # Save
    output_file = 'gdp_history_2021_2025.csv'
    df_merged.to_csv(output_file, index=False)
    print(f"Successfully saved merged data to {output_file}")
    print(df_merged.head(10))

if __name__ == "__main__":
    main()
