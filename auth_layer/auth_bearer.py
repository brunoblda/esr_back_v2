#The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2, APIKeyCookie
from starlette.datastructures import MutableHeaders

from .jwt_class import authentication 


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        if(request.cookies.get("Authorization")):
            new_header = MutableHeaders(request._headers)
            new_header["Authorization"] = request.cookies.get("Authorization")
            request._headers = new_header
        credentials: HTTPAuthorizationCredentials  = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return True
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            authentication_var = authentication(jwtoken)
        except:
            authentication_var = None
        if authentication_var:
            isTokenValid = True
        return isTokenValid