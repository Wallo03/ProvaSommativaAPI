from fastapi import FastAPI, Request, Form, Depends,HTTPException,status
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
import joblib
import uvicorn

app = FastAPI(title="Startup of BirdIT", description="with FastAPI by Waldo Bird", version="1.0")

## Basemodel
class StartupData(BaseModel):
    rdspend: float =73721
    administration: float =121344
    marketingspend: float =211025


# JINJA2
templates = Jinja2Templates(directory="templates")

## blocco per la cache del mio modello
@app.on_event("startup")
def startup_event():
    "modello *.pkl di ML"
    global model # la varibile dovrà essere globale
    model = joblib.load("startup.pkl")
    print(" MODEL LOADED!!")
    return model

##########################################################################################################
################################# SERVER JINJA2 + INFERENCE ##############################################

@app.get("/",status_code=200)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict")
async def predict(request: Request,rd: float = Form(...), #<input name ="sepal_len">
                             admin: float = Form(...), #<input name ="sepal_wid">
                             marksd: float = Form(...), #<input name ="petal_len">
                            ):
    #target_names = load_iris().target_names.tolist()
    target_names = ['R&D Spend', 'Administration', 'Marketingspend']
    data = StartupData(rdspend=rd, administration=admin, marketingspend=marksd)
    X = [[data.rdspend, data.administration, data.marketingspend]]
    y_pred = model.predict(X)
    prediction = Prediction(target=y_pred[0], target_names=target_names)
    return templates.TemplateResponse("home.html", {"request": request,"prediction": prediction})

##########################################################################################################
################################# CHIAMATE DIRETTE GET POST ##############################################

@app.get("/")
def home():
    return {" ---->          http://localhost:8000/docs     <----------"}

## secca GET per streamlit o chiamate esterne
@app.get("/predict2")
async def predictget(data:StartupData=Depends()):
    try:
        X = [[data.rdspend, data.administration, data.marketingspend]]
        y_pred = model.predict(X)[0]
        res = round(y_pred,2)
        return {'prediction':res}
    except:
        raise HTTPException(status_code=404, detail="error")

## secca POST per streamlit o chiamate esterne
@app.post("/predict")
async def predictpost(data:StartupData):
    try:
        X = [[data.rdspend, data.administration, data.marketingspend]]
        y_pred = model.predict(X)[0]
        res = round(y_pred,2)
        return {'prediction':res}
    except:
        raise HTTPException(status_code=404, detail="error")

###############################################################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
