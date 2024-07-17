from datetime import datetime
from typing import List

from pydantic import BaseModel


class PriceList(BaseModel):
    id: int
    currency: str
    date_: datetime
    price: float


class PriceResponse(BaseModel):
    currency: str
    price: float


class PriceHistoryResponse(BaseModel):
    prices: List[PriceList]


class SuccessResponse(BaseModel):
    status: str
