# %%
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import os

# %%
def generateStatmuseUrl(playerName): 
    """Generate StatMuse URL using the name directly from Excel"""
    if pd.isna(playerName):
        return None
    nameForUrl = playerName.strip().lower().replace(' ', '-')
    return f"https://www.statmuse.com/nfl/ask/{nameForUrl}-stats-career"


# %%

def getPlayerGames(playerName):
    url = generateStatmuseUrl(playerName)
    if not url:
        return 0, None, "No valid URL"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    } # act as a browser to nbot get blocked
    #https://www.zenrows.com/blog/user-agent-web-scraping#how-to

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser') 
            for table in soup.find_all('table'):
                trs = table.find_all('tr')
                if trs:
                    lastTr = trs[-1] #Career stats were always last here
                    tds = lastTr.find_all('td')
                    for i, td in enumerate(tds): #enumerate to get index
                        text = td.get_text(strip=True)
                        if text.isdigit():
                            num = int(text) 
                            if 0 <= num <= 400 and i <= 8: # most games ever played isless than 400
                                return num, url, "yippee!!!!!!!"
            return 0, url, "No games"
        else:
            return 0, url, f"HTTP {response.status_code}"
    except Exception as e:
        return 0, url, f"Error: {str(e)}"
    return 0, url, "Unknown Error"

# %%
def processCsvWithGames(inputPath, outputPath=None, startFrom=0): #put all results into column in csv
    print(f"Reading CSV from: {inputPath}")
    df = pd.read_csv(inputPath)
    print(f"Total players in CSV: {len(df)}")

    for col in ['statmuse_url', 'games_played', 'scrape_status']:
        if col not in df.columns:
            df[col] = '' if col != 'games_played' else 0 # create the column

    if outputPath is None:
        outputPath = inputPath.replace('.csv', '_with_games.csv') #create new output

    successful, failed, skipped = 0, 0, 0

    print("==========" )

    for idx in range(startFrom, len(df)):
        playerName = df.at[idx, 'nameFull']
        if pd.notna(df.at[idx, 'games_played']) and df.at[idx, 'scrape_status'] == 'yippee!!!!!!!':
            skipped += 1
            print(f"[{idx + 1}/{len(df)}] Skipping {playerName} - already processed")
            continue

        if pd.isna(playerName):
            df.at[idx, 'scrape_status'] = 'No name'
            failed += 1
            continue

        print(f"Processing: {playerName}")
        games, url, status = getPlayerGames(playerName)
        df.at[idx, 'statmuse_url'] = url or ''
        df.at[idx, 'games_played'] = games
        df.at[idx, 'scrape_status'] = status

        if status == 'yippee!!!!!!!':
            successful += 1
            print(f"  Found: {games} games")
        else:
            failed += 1
            print(f"  Failed: {status}")

        if (idx - startFrom + 1) % 25 == 0: # saves progress incase power goes out
            df.to_csv(outputPath, index=False)
            rate = successful / (successful + failed) * 100 if (successful + failed) else 0
            print(f" Progress saved. Success rate: {rate:.2f}% ")

        if idx < len(df) - 1: # pause after each player so no rate limiting
            time.sleep(4)

        if status == "Rate limited" and failed > 10 and successful == 0:
            print("Too many rate limit errors. Stopping to avoid blocking.")
            break

    df.to_csv(outputPath, index=False)

    print("==========" )    
    print("WE DONE")
    print("==========" ) 
    return df

# %%
if __name__ == "__main__":
    inputCsv = r"\draftAndCombine.csv"
    outputCsv = r"\draftAndCombineAndGames.csv"

    print("")
    
    processCsvWithGames(inputCsv, outputCsv)
    # resumeProcessing(inputCsv, outputCsv)



