from pydantic import BaseModel, Field
from typing import Optional


class ExpenseSchema(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)


class ExpenseResponseSchema(BaseModel):
    id: int = Field(..., gt=0)
    description: str
    amount: float


class ExpenseUpdateSchema(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
