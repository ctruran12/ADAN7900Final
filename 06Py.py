# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR


# %%
df = pd.read_csv(r"\finalEstimateSuccess.csv")

numericCols = ['athleticScore0to10', 'draftTradeValue']

x = df[numericCols]
y = pd.to_numeric(df['success_score'])


preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numericCols) #standardized num cols
])

# %%

models = {
    'Ridge': Ridge(),
    'Lasso': Lasso(),
    'RandomForest': RandomForestRegressor(),
    'SVR': SVR(),
    'DecisionTree': DecisionTreeRegressor(),
}

XTrain, XTest, yTrain, yTest = train_test_split(x, y, test_size=0.15, random_state=627)

# %%
results = []
for name, model in models.items(): 
    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', model)
    ])
    pipe.fit(XTrain, yTrain)
    yPred = pipe.predict(XTest)
    results.append({
        'Model': name,
        'R2 Score': r2_score(yTest, yPred),
        'MAE': mean_absolute_error(yTest, yPred)
    })

resultsDf = pd.DataFrame(results)
print(resultsDf.sort_values(by='R2 Score', ascending=False))


# %%
ridge = Ridge()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(XTrain)
ridge.fit(X_scaled, yTrain)

for name, coef in zip(numericCols, ridge.coef_):
    print(name, coef)



