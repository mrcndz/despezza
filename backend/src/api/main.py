from fastapi import FastAPI
from src.core.database import engine, Base
from src.api.routers import users, groups, expenses, credit_cards, incomes, recurring_expenses, expense_categories, income_categories

from src.core.database import create_tables

create_tables()

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(groups.router, prefix="/groups", tags=["Groups"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(credit_cards.router, prefix="/credit_cards", tags=["Credit Cards"])
app.include_router(incomes.router, prefix="/incomes", tags=["Incomes"])
app.include_router(recurring_expenses.router, prefix="/recurring_expenses", tags=["Recurring Expenses"])
app.include_router(expense_categories.router, prefix="/expense_categories", tags=["Expense Categories"])
app.include_router(income_categories.router, prefix="/income_categories", tags=["Income Categories"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Despezza API"}
