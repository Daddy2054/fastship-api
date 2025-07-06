from typing import Annotated

# from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends

from app.database.redis import add_jti_to_blacklist

# from app.database.models import Seller

from ..dependencies import SellerServiceDep, get_seller_access_token  # , SessionDep
from ..schemas.seller import SellerCreate, SellerRead

# from app.core.security import oauth2_scheme
# from app.utils import decode_access_token

router = APIRouter(prefix="/seller", tags=["Seller"])


### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add(seller)


### Login the seller
@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }


""" ### Get seller details
curl http://127.0.0.1:8000/seller/token \
  --request POST \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'username=seller1@example.com' \
  --data-urlencode 'password=string' \
  --data-urlencode 'scope=' \
  --data-urlencode 'client_id=' \
  --data-urlencode 'client_secret='
  """


# @router.get("/dashboard")
# async def get_dashboard(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     session: SessionDep,
# ) -> Seller | dict[str, str]:

#     data = decode_access_token(token)

#     if not data:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid token",
#         )
#     # Here you can add logic to fetch seller details or perform actions based on the token
#     seller = await session.get(Seller, data["user"]["id"])

#     return seller or {"message": "Seller not found"}


### Logout a seller
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
