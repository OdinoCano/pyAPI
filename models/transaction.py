from pydantic import BaseModel, Field
from typing import Optional

class Transaction(BaseModel):
	id: Optional[int] = None
	firstName: str = Field(min_length=1, max_length=255)
	lastName: str = Field(min_length=1, max_length=255)
	email: str = Field(default="a@a.a", min_length=5, max_length=255)
	token: str = Field(default="", min_length=32, max_length=32)
	time: int = Field(default=0, gt=0)
	passwd: str = Field(min_length=8, max_length=255)
