import numpy as np
import pandas as pd
import joblib

df=pd.read_csv("Iris.csv")
df=df.drop('Id', axis=1)

x=df.drop('Species', axis=1)
y=df['Species']

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=42)

from sklearn.ensemble import RandomForestClassifier
model=RandomForestClassifier(random_state=42)
model.fit(x_train,y_train)

joblib.dump(model, "baseline_model.pkl")

# Save test data (simulated "new incoming data")
np.save("new_data_X.npy", x_test.values)
np.save("new_data_y.npy", y_test.values)

print("Model trained and saved!")






