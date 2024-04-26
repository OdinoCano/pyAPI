from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
	id: Optional[int] = None
	email: str = Field(default=None, min_length=5, max_length=255)
	passwd: str = Field(default=None, min_length=8, max_length=255)
	firstName: str = Field(default=None, min_length=1, max_length=255)
	lastName: str = Field(default=None, min_length=1, max_length=255)
