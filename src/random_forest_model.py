import pickle

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from constants import *

SOURCE_FILE_DATE = "2022-10-30-15-30-30"

with open(f"{DATA_DIR}/final_data.csv", "r") as combined_data:
    df = pd.read_csv(combined_data, index_col=0)

df = df.dropna()

y =  pd.DataFrame(df, columns=["ACTUAL_DELIVERY_MINUTES"]).reset_index()
df = df.drop(columns=["Unnamed: 0", "TIMESTAMP", "ACTUAL_DELIVERY_MINUTES"])
df = df.reset_index()

x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.1, random_state=10)

rf = RandomForestRegressor(n_estimators = 1000, max_features='sqrt', n_jobs=-1, random_state=10)
rf.fit(x_train, y_train)

predictions = rf.predict(x_test)[:, 1]
predictions=predictions.reshape(len(predictions),1)

orig_estimates = pd.DataFrame(df["ESTIMATED_DELIVERY_MINUTES"]).reset_index()
orig_errors = abs(y["ACTUAL_DELIVERY_MINUTES"] - orig_estimates["ESTIMATED_DELIVERY_MINUTES"])
print(f"Original Mean Absolute Error: {np.mean(orig_errors)}, Standard deviation: {np.std(orig_errors)}\n")

errors = abs(y_test - predictions)["ACTUAL_DELIVERY_MINUTES"]
print(f"Model's Mean Absolute Error: {np.mean(errors)}, Standard deviation: {np.std(errors)}")

with open("random_forest.model", "wb") as f:
    pickle.dump(rf, f)
