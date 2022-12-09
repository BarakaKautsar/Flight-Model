import pandas as pd
import numpy as np
import joblib
import schemas
# import time
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.pipeline import Pipeline 
# from sklearn.compose import ColumnTransformer
# from sklearn import linear_model
# from sklearn.linear_model import LinearRegression
# from sklearn import *



file = open("models/flightmodel.joblib","rb")
model = joblib.load(file)
types = {
    "Quarter": np.float64,
    "Origin": str,
    "Dest": str,
    "NumTicketsOrdered": np.float64,
    "AirlineCompany": str,
}
# test_data = plan.split(",")
# df = pd.DataFrame(test_data).transpose()
# df.columns = list(types.keys())
# df = df.astype(types)
# df.to_numpy()
input = schemas.Plan(Quarter=1,Origin="SFO",Dest="LAX",NumTicketsOrdered=2,AirlineCompany="AA")
input_arr = [input.Quarter,input.Origin,input.Dest,input.NumTicketsOrdered,input.AirlineCompany]
df = pd.DataFrame(input_arr).transpose()
df.columns = list(types.keys())
df = df.astype(types)
df.to_numpy()
predict = "$" + str(round(model.predict(df)[0][0], 2))
print(predict)