# %%
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# %%
df = pd.read_csv(r"\draftAndCombineAndGames.csv")

positionMap = { #maps individual positions to their group i wanna use for their athletic score
    'WR': 'WR',
    'RB': 'RB',
    'CB': 'DB', 'FS': 'DB', 'SS': 'DB', 'DB': 'DB',
    'QB': 'QB',
    'TE': 'TE',
    'EDGE': 'EDGE', 'DE': 'EDGE', 'LE': 'EDGE', 'RE': 'EDGE', 'OLB': 'EDGE',
    'LB': 'MLB', 'MLB': 'MLB', 'WLB': 'MLB'
}

df['positionGroup'] = df['combinePosition'].map(positionMap)
df = df[df['positionGroup'].notna()].copy()


metrics = [
    'combine40yd', 'combineVert', 'combineBench',
    'combineShuttle', 'combineBroad', 'combine3cone',
    'heightInches', 'weight'
]

df['validTestCount'] = df[metrics].notna().sum(axis=1)
df = df[df['validTestCount'] >= 3].copy()

metricsDir = {
    'combine40yd': '-z', #some workouts it is better to have a lower score, so the z is negative because the lower will be more athletic
    'combineVert': 'z', #Vertical is the opposite where higher is better
    'combineBench': 'z',
    'combineShuttle': '-z',
    'combineBroad': 'z',
    'combine3cone': '-z',
    'heightInches': 'z',
    'weight': 'z'
}

scoreColumns = []
for metric, direction in metricsDir.items():  
    zCol = f"{metric}Z" #example 40yarddashZ
    scoreColumns.append(zCol)
    df[zCol] = np.nan #new column for the new scores
    for group in df['positionGroup'].unique():
        groupMask = df['positionGroup'] == group
        vals = df.loc[groupMask, metric]
        scaler = StandardScaler()
        z = scaler.fit_transform(vals.values.reshape(-1, 1)).flatten()
        if direction == '-z':
            z *= -1 #make the z positive now
        df.loc[groupMask, zCol] = z

df['positionAthleticScore'] = df[scoreColumns].mean(axis=1, skipna=True)

df['athleticScore0to10'] = df['positionAthleticScore'].rank(pct=True) * 10 # turns into 0-10 scale 

# Save it
df.to_csv(r"\draftCombineAthleticScore.csv", index=False)

print("done done done")



