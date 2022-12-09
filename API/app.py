from fastapi import FastAPI, Request
import joblib
import uvicorn
import schemas 
import numpy as np
import pandas as pd


app = FastAPI()


@app.get("/")
async def dashboard(request: Request):
    return {
       "message": "Please enter your travel plan in the following format: Quarter,Origin,Destination,Number of ticket,Airline. For example: 1,BOS,LAX,2,AA"
    }



@app.get("/PricePredict/")
async def predict(plan: str):
    file = open("models/flightmodel.joblib","rb")
    model = joblib.load(file)

    # input = {"data": plan}
    types = {
        "Quarter": np.float64,
        "Origin": str,
        "Dest": str,
        "NumTicketsOrdered": np.float64,
        "AirlineCompany": str,
    }
    
    data = plan.split(",")
    df = pd.DataFrame(data).transpose()
    df.columns = list(types.keys())
    df = df.astype(types)
    df.to_numpy()

    predict = "$" + str(round(model.predict(df)[0][0], 2))
    
    return {"Your predicted price will be:": predict}

@app.post("/Predict/")
async def predict(input: schemas.Plan):
    file = open("models/flightmodel.joblib","rb")
    model = joblib.load(file)

    types = {
    "Quarter": np.float64,
    "Origin": str,
    "Dest": str,
    "NumTicketsOrdered": np.float64,
    "AirlineCompany": str,
    }

    input_arr = [input.Quarter,input.Origin,input.Dest,input.NumTicketsOrdered,input.AirlineCompany]
    df = pd.DataFrame(input_arr).transpose()
    df.columns = list(types.keys())
    df = df.astype(types)
    df.to_numpy()

    predict = "$" + str(round(model.predict(df)[0][0], 2))
    return {"Your predicted price will be:": predict}


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")