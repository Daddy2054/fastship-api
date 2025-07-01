from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Seller, Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session

    # Get a shipment by id 
    async def get(self, id: int) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise ValueError(f"Shipment with id {id} not found")
        return shipment

    # Add a new shipment
    async def add(self, shipment_create: ShipmentCreate, seller: Seller
                  ) -> Shipment:
        """
            **shipment_create.model_dump(exclude_unset=True),

        Args:
            shipment_create (ShipmentCreate): The data required to create a new shipment.

        Returns:
            Shipment: The newly created shipment object.
        """
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,  # Associate the shipment with the seller
        )
        self.session.add(new_shipment)
        await self.session.commit()
        # Refresh the session to get the latest state of the new shipment
        await self.session.refresh(new_shipment)

        return new_shipment

    # Update an existing shipment
    async def update(self, id: int, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        """
            Update an existing shipment with the provided data.

        Args:
            id (int): The ID of the shipment to update.
            shipment_update (dict): The data to update the shipment with.

        Returns:
            Shipment: The updated shipment object.
        """
        if shipment_update.get("status") is not None:
            shipment.status = ShipmentStatus(shipment_update["status"])
        if shipment_update.get("estimated_delivery") is not None:
            shipment.estimated_delivery = datetime.fromisoformat(
                shipment_update["estimated_delivery"]
            )

        # Commit the changes to the database
        await self.session.commit()
        # Refresh the session to get the latest state of the shipment
        await self.session.refresh(shipment)

        # Return the updated shipment object
        return shipment

    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self.session.delete(await self.get(id))
        await self.session.commit()