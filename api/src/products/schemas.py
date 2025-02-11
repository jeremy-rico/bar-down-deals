from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WebsiteBase(BaseModel):
    """Base schema for Website data.

    Attributes:
        name: The website's name (defined in spider)
        url: The website's base url
             min length = len(https://a.com)
             max length = none
        last_scraped: Timestamp
    """

    name: str = Field(min_length=1, max_length=255, description="The website's name")
    url: str = Field(min_length=13, description="The website's base url")
    last_scraped: datetime = Field(
        default=datetime.now(), description="Timestamp of when site was last scraped"
    )


class WebsiteCreate(WebsiteBase):
    """Schema for creating a new hero."""


# class WebsiteUpdate(BaseModel):
#     """Schema for updating an existing hero.
#
#     All fields are optional since updates might be partial.
#     """
#
#     name: str | None = Field(None, min_length=1, max_length=100)
#     alias: str | None = Field(None, min_length=1, max_length=100)
#     powers: str | None = None
#
#
# class HeroResponse(HeroBase):
#     """Schema for hero responses.
#
#     Includes all base fields plus the id.
#     """
#
#     model_config = ConfigDict(from_attributes=True)
#     id: int
