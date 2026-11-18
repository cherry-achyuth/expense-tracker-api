from fastapi import FastAPI,HTTPException,Depends,Query
from app.database import get_db
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from app.models import ExpenseModel
from app.schemas import ExpenseCreate,ExpenseResponse,ExpensePage,ExpenseSummary
import logging

logging.basicConfig(level=logging.INFO)
logger =  logging.getLogger(__name__)


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

@app.get("/expenses/summary", response_model=ExpenseSummary)
def get_expense_summary(db: Session = Depends(get_db)):

    # 1. Count all expenses
    total_expenses = db.scalar(
        select(func.count()).select_from(ExpenseModel)
    )

    # 2. Calculate total spending
    total_amount = db.scalar(
        select(
            func.coalesce(func.sum(ExpenseModel.amount), 0)
        )
    )

    # 3. Calculate spending category-wise
    statement = (
        select(
            ExpenseModel.category,
            func.sum(ExpenseModel.amount).label("total")
        )
        .group_by(ExpenseModel.category)
        .order_by(ExpenseModel.category)
    )

    category_rows = db.execute(statement).all()

    # 4. Prepare the API response
    return {
        "total_expenses": total_expenses,
        "total_amount": total_amount,
        "category_summary": [
            {
                "category": row.category,
                "total": row.total
            }
            for row in category_rows
        ]
    }

@app.get('/expenses',response_model = ExpensePage)
def get_expenses(category : str|None = None,
                 skip : int = Query(default = 0,ge=0),
                 limit : int = Query(default = 10,ge=0,lt=100),
                 db:Session = Depends(get_db)):
    'returns the expenses data'

    statement = select(ExpenseModel)

    if category:
        statement = statement.where(ExpenseModel.category == category)

    count_statement = (select(func.count()).select_from(ExpenseModel))

    if category:
        count_statement = count_statement.where(ExpenseModel.category == category)

    total = db.scalar(count_statement)

    statement = (statement.order_by(ExpenseModel.id)
                 .offset(skip)
                 .limit(limit))
    expenses = db.scalars(statement).all()

    return {
        "items" : expenses,
        "total" : total,
        "skip" : skip,
        "limit":limit
    }

@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=201
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    try:
        new_expense = ExpenseModel(
            title=expense.title,
            amount=expense.amount,
            category=expense.category
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense

    except Exception:
        db.rollback()

        logger.exception("failed to create expense")
        raise HTTPException(
            status_code=500,
            detail="Failed to create expense"
        )

@app.put('/update-expense/{expense_id}',response_model = ExpenseResponse)
def update_expense(upd_expense:ExpenseCreate,expense_id:int,db:Session = Depends(get_db)):
    expense = db.get(ExpenseModel,expense_id)
    if expense is None:
        raise HTTPException(status_code=404,detail="expense not found")
    
    expense.title = upd_expense.title
    expense.amount = upd_expense.amount
    expense.category =  upd_expense.category

    db.commit()
    db.refresh(expense)
    return expense

@app.delete('/delete-expense/{expense_id}')
def delete_expense(expense_id:int,db:Session = Depends(get_db)):
    expense = db.get(ExpenseModel,expense_id)
    if expense is None:
        raise HTTPException(status_code=404,detail='expense not found')

    db.delete(expense)
    db.commit()

    return {"message" : "expense deleted successfully"}
