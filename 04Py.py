# %%
import pandas as pd

df = pd.read_csv(r"\draftCombineAthleticScore.csv")
careerAwards = pd.read_csv(r"\careerAccolades.csv")#data was aggregated in Excel

# Join
df = df.merge(careerAwards, on='playerId', how='left')

# Fill empty/missing values with 0s
df['mvp'] = pd.to_numeric(df.get('MVP', 0), errors='coerce').fillna(0)
df['apAllProFlag'] = pd.to_numeric(df.get('AP_All_Pro_Flag', 0), errors='coerce').fillna(0)
df['proBowlYear'] = pd.to_numeric(df.get('ProBowlYear', 0), errors='coerce').fillna(0)
df['gamesPlayed'] = pd.to_numeric(df.get('games_played', 0), errors='coerce').fillna(0)

# Scoring system
df['successScore'] = (
    df['mvp'] * 9 +
    df['apAllProFlag'] * 4.5 +
    df['proBowlYear'] * 2.5 +
    df['gamesPlayed'] * 0.05
)

df.to_csv(r"\careerDraftCombine.csv", index=False)

print("saved")



