from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import pandas as pd
import joblib 

df = pd.read_csv("DATA/Final_data.csv")

X = df.drop(columns=['PRIX'])
y = df['PRIX']

gradiantB_model=GradientBoostingRegressor(learning_rate= 0.1, max_depth=5,n_estimators=100)
print(X.columns)
gradiantB_model.fit(X,y)

# Save the model as a joblib file
joblib.dump(gradiantB_model, 'model.joblib')
