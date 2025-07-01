from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.utils import decode_access_token


# Asynchronous database session dep annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# Access token data dep
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]) :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    return data


# Logged In Seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)],
    session: SessionDep,
):
    return await session.get(Seller, UUID(token_data["user"]["id"]))


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


# Seller dep
SellerDep = Annotated[
    Seller,
    Depends(get_current_seller),
]

# Shipment service dep annotation
ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]
# Seller service dep annotation
SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]
