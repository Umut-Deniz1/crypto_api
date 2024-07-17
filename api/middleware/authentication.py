from fastapi import Header, HTTPException

from api.conf.settings import Settings

settings = Settings()


class TokenAuthentication:
    @classmethod
    async def verify_token(cls, x_authorization: str = Header()):
        if x_authorization != settings.CLIENT_X_AUTH:
            raise HTTPException(status_code=401, detail="UNAUTHORIZED_TOKEN")
