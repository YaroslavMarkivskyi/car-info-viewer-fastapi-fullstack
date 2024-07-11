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


@app.get("/cars/{car_id}", response_model=Car)
def get_car_by_id(car_id: int = Path(...,ge=0, lt=1000)):
    car = cars.get(car_id)
    if not car:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Could not find car by ID.")
    return car
