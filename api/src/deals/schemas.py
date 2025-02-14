from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DealBase(BaseModel):
    """
    Base model for Deal data
    """

    # Product atts
    # product_name: str
    # brand: str
    # # category:
    # image_url: str
    # description: str
    # created_at: datetime
    #
    # # Website atts
    # website_name: str
    # website_url: str

    # Deal atts
    product_id: int
    website_id: int
    price: float
    original_price: Optional[float]
    discount: Optional[float]
    url: str
    scraped_at: datetime


class DealCreate(DealBase):
    """
    Schema for creating new deal
    """


class DealUpdate(BaseModel):
    """
    Schema for updating an existing deal
    """

    pass


class DealResponse(DealBase):
    """
    Schema for deal response

    Includes all base fields plus id
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
