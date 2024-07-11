from typing import Optional, List

from pydantic import BaseModel, Field


class Car(BaseModel):
    make: str
    model: str
    year: str = Field(..., ge=1970, lt=2022)
    price: str
    engine: Optional[str] = 'V4'
    autonomous: bool
    sold: List[str]
