from pydantic import BaseModel, Field
from typing import Optional

class APIKey(BaseModel):
	user: str = Field(min_length=5, max_length=255)
	passwd: str = Field(min_length=8, max_length=255)
