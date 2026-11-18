from sqlalchemy import String,Integer,Numeric
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base
from decimal import Decimal


class ExpenseModel(Base):
    __tablename__ = 'expenses'

    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str] = mapped_column(String(50),nullable =False)
    amount : Mapped[Decimal] = mapped_column(Numeric(10,2),nullable = False)
    category : Mapped[str] = mapped_column(String(50),nullable = False)
