from pydantic import BaseModel
from sqlmodel import Field


# =========================== Search Parameter Model ====================
class SearchParams(BaseModel):
    """
    page: pagination
    limit: max items per response
    query: search query string
    """

    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    q: str = Field(min_length=3, max_length=255)
