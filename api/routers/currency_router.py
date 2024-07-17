from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.conf.settings import Settings
from api.db.database import get_db
from api.middleware.authentication import TokenAuthentication
from api.serializers.currency_serializer import (PriceHistoryResponse,
                                                 PriceResponse,
                                                 SuccessResponse)
from api.services.currency import CurrencyService

settings = Settings()

currency_router = APIRouter(
    dependencies=[Depends(TokenAuthentication.verify_token)],
    prefix=settings.API_STR,
    tags=["Currency"],
)


def get_service(db: Session = Depends(get_db)) -> CurrencyService:
    service = CurrencyService(db)
    return service


@currency_router.get("/price", response_model=PriceResponse)
async def get_price(
    currency: str,
    service: CurrencyService = Depends(get_service),
):
    response = await service.get_price(currency=currency)
    return response


@currency_router.get("/price/history", response_model=PriceHistoryResponse)
async def get_price_history(
    page: int = 1,
    service: CurrencyService = Depends(get_service),
):
    response = await service.get_price_history(page=page)
    return response


@currency_router.delete("/price/history", response_model=SuccessResponse)
async def delete_price_history(
    service: CurrencyService = Depends(get_service),
):
    response = await service.delete_price_history()
    return response
