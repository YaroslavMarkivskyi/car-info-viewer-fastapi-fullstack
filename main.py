from typing import Optional, List, Dict

from fastapi import FastAPI, Query, Path, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder

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
def get_car_by_id(car_id: int = Path(..., ge=0, lt=1000)):
    car = cars.get(car_id)
    if not car:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Could not find car by ID.")
    return car


@app.post("/cars", status_code = status.HTTP_201_CREATED)
def add_cars(body_cars: List[Car], min_id: Optional[int] = Body(0)):
    if len(cars) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cars to add.")
    min_id = len(cars.values()) + min_id
    for car in body_cars:
        while cars.get(min_id):
            min_id += 1
        cars[min_id] = car
        min_id += 1


@app.put("/cars/{car_id}", response_model=Dict[str, Car])
def update_car(car_id: int, car: Car = Body(...)):
    stored = cars.get(car_id)
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find car with given ID.")
    stored = Car(**stored)
    new = car.dict(exclude_unset=True)
    new = stored.copy(update=new)
    cars[car_id] = jsonable_encoder(new)
    response = {}
    response[car_id] = cars[car_id]
    return response


@app.delete("/cars/{id}")
def delete_car(car_id: int):
    if not cars.get('id'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find car with given ID.")
    del cars[car_id]
