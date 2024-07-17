import asyncio
from datetime import datetime, timedelta

import ccxt
from ccxt.base.errors import ExchangeError
from fastapi import HTTPException
from sqlalchemy import delete

from api.models import Currency
from api.serializers.currency_serializer import (PriceHistoryResponse,
                                                 PriceList, PriceResponse,
                                                 SuccessResponse)


class CurrencyService:
    def __init__(self, db):
        self.db = db
        self.exchange = ccxt.kucoin()

    @staticmethod
    def _round_to_seconds(dt: datetime) -> datetime:
        return dt - timedelta(microseconds=dt.microsecond)

    async def fetch_price_from_ccxt(self, currency: str) -> float:
        try:
            symbol = f"{currency}/USDT"
            loop = asyncio.get_event_loop()
            ticker = await loop.run_in_executor(None, self.exchange.fetch_ticker, symbol)
            return ticker["last"]
        except ExchangeError:
            raise HTTPException(status_code=400, detail="Currency not found")

    async def get_price(self, currency: str) -> PriceResponse:
        current_date = self._round_to_seconds(datetime.utcnow())
        result = self.db.query(Currency).filter_by(currency=currency).order_by(Currency.date_.desc())
        record = result.first()
        if record and (current_date - record.date_).total_seconds() < 10:
            return PriceResponse(currency=record.currency, price=record.price)
        last_price = await self.fetch_price_from_ccxt(currency)
        new_record = Currency(currency=currency, price=last_price, date_=current_date)
        self.db.add(new_record)
        self.db.commit()
        return PriceResponse(currency=new_record.currency, price=new_record.price)

    async def get_price_history(self, page: int) -> PriceHistoryResponse:
        result = self.db.query(Currency).order_by(Currency.date_.desc()).offset((page - 1) * 10).limit(10)
        records = result.all()
        prices = [
            PriceList(id=record.id, currency=record.currency, date_=record.date_, price=record.price)
            for record in records
        ]
        return PriceHistoryResponse(prices=prices)

    async def delete_price_history(self) -> SuccessResponse:
        stmt = delete(Currency)
        self.db.execute(stmt)
        self.db.commit()
        return SuccessResponse(status="success")
