from pydantic import BaseModel, Field
from typing import Optional

class Link(BaseModel):
	apikey: int
	institution: str = Field(min_length=1, max_length=255)
	user: str = Field(min_length=1, max_length=255)
	passwd: str = Field(default=None,min_length=1, max_length=255)
