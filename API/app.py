from fastapi import FastAPI, Request, Body, Depends
import joblib
import uvicorn
import schemas 
import numpy as np
import pandas as pd

import database.services

from typing import List
import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm


app = FastAPI()


@app.get("/",tags=["Dashboard"])
async def dashboard(request: Request):
    return {
       "message": "Hello, welcome to flight price predictions"
    }

@app.post("/api/users",tags=["Authentication"])
async def create_user(user: schemas.UserCreate, db: _orm.Session = _fastapi.Depends(database.services.get_db)):
    db_user = await database.services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400,
            detail="User with that email already exists")

    user = await database.services.create_user(user=user, db=db)

    return await database.services.create_token(user=user)


@app.post("/api/token",tags=["Authentication"])
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(database.services.get_db)):
    user = await database.services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await database.services.create_token(user=user)


@app.get("/api/users/me",tags=["Service"], response_model=schemas.User)
async def get_user(user: schemas.User = _fastapi.Depends(database.services.get_current_user)):
    return user



@app.post("/Predict/",tags=["Service"],dependencies= [Depends(database.services.get_current_user)])
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
    uvicorn.run(app="app:app", port=8080, host="0.0.0.0",reload=True)