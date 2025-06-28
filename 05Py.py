# %%
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv(r"\careerDraftCombine.csv")

# Ensure numeric inputs (simplified if data is clean)
df['athleticScore0to10'] = pd.to_numeric(df['athleticScore0to10']).fillna(0)
df['draftTradeValue'] = pd.to_numeric(df['draftTradeValue']).fillna(0)
df['successScore'] = pd.to_numeric(df['success_score']).fillna(0)


x = df[['athleticScore0to10', 'draftTradeValue']]
y = df['successScore']

# super simple model
model = LinearRegression()
model.fit(x, y)
df['estimatedSuccessScore'] = model.predict(x)
df['performanceDiff'] = df['successScore'] - df['estimatedSuccessScore']

df.to_csv(r"\finalEstimateSuccess.csv", index=False)

print("saved")



