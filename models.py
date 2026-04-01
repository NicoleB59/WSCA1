# Pydantic Models
from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt, field_validator
from decimal import Decimal

class ProductCreate(BaseModel):
    ProductID: PositiveInt
    Name: str = Field(..., min_length=1, max_length=200)
    UnitPrice: Decimal = Field(..., gt=0)
    StockQuantity: NonNegativeInt
    Description: str = Field(..., min_length=1, max_length=1000)

    @field_validator("Name", "Description")
    @classmethod
    def not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class ProductIDModel(BaseModel):
    product_id: PositiveInt


class StartsWithModel(BaseModel):
    letter: str = Field(..., min_length=1, max_length=1)

    @field_validator("letter")
    @classmethod
    def must_be_alpha(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("letter must be a single alphabet character")
        return value


class PaginateModel(BaseModel):
    start_id: PositiveInt
    end_id: PositiveInt