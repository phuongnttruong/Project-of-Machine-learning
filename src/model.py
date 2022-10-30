import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("../data/combined_data_2022-10-30-15-30-30.csv")

# create pipeline
pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression()
    )

# get training data and test data
train, test = train_test_split(df, random_state=0)

# fit training data  ---- IMPLEMENT REQUIRED --- FIND BEST MODEL
pipe.fit(train)
Pipeline(steps=[('standardscaler', StandardScaler()),
                ('logisticregression', LogisticRegression())])

# use test data to provide actual delivery time
