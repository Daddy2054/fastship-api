# from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer #, HTTPBearer

# from app.utils import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/token")

# class AccessTokebBearer(HTTPBearer):
#     async def __call__(self, request):
#         token = await super().__call__(request)

#         token_data = decode_access_token(token.credentials)


#         if token_data is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Not authorized!",
#             )
 
#         return token_data
    
# access_token_bearer = AccessTokebBearer()