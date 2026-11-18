from pydantic import BaseModel,Field,ConfigDict
from decimal import Decimal

class ExpenseCreate(BaseModel):
    title : str = Field(min_length=1,max_length=100)
    amount : Decimal =  Field(ge=0,decimal_places=2,max_digits=10)
    category : str = Field(min_length=1,max_length=50)

class ExpenseResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    amount : Decimal
    category : str

class ExpensePage(BaseModel):
    items : list[ExpenseResponse]
    total : int
    skip : int
    limit : int

class CategorySummary(BaseModel):
    category: str
    total: Decimal


class ExpenseSummary(BaseModel):
    total_expenses: int
    total_amount: Decimal
    category_summary: list[CategorySummary]