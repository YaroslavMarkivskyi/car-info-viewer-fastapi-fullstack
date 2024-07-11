from typing import Optional, List, Dict

from fastapi import FastAPI, Query, Path, HTTPException, status, Body

from database import cars
from models import Car


app = FastAPI()


@app.get("/cars", response_model=List[Dict[str, Car]])
def get_cars(number: Optional[str] = Query("10", max_length=3)):
    response = []
    for id, car in list(cars.items())[:int(number)]:
        to_add = {}
        to_add[id] = car
        response.append(to_add)
    return response




