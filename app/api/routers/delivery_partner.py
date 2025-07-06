from typing import Annotated

# from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

# from app.api.schemas.delivery_partner import DeliveryPartnerRead, DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist

# from app.database.models import Seller

from ..dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    SellerServiceDep,
    get_partner_access_token,
)
from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
# from app.core.security import oauth2_scheme
# from app.utils import decode_access_token

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Register a delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    seller: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(seller)


### Login the delivery partner
@router.post("/token")
async def login_delivery_partner(
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

### Update the logged in delivery partner
@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    # Update data with given fields
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    return await service.update(
        partner.sqlmodel_update(update),
    )

### Logout a delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
