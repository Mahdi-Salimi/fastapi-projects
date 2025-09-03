from fastapi import FastAPI, HTTPException, status
from typing import Dict, List

from schema import ExpenseSchema, ExpenseResponseSchema, ExpenseUpdateSchema

app = FastAPI(title="Expense Manager API")

expenses: Dict[int, dict] = {}
next_id: int = 1 


@app.post("/expenses", response_model=ExpenseResponseSchema, status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseSchema):
    global next_id

    description = data.description
    amount = data.amount

    if description is None or amount is None:
        raise HTTPException(status_code=400, detail="description and amount are required")

    expense = {"id": next_id, "description": description, "amount": float(amount)}

    expenses[next_id] = expense
    next_id += 1
    return expense


@app.get("/expenses", response_model=List[ExpenseResponseSchema], status_code=status.HTTP_200_OK)
def get_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema, status_code=status.HTTP_200_OK)
def update_expense(expense_id: int, data: ExpenseUpdateSchema):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense = expenses[expense_id]
    if data.description is not None:
        expense["description"] = data.description
    if data.amount is not None:
        expense["amount"] = float(data.amount)

    expenses[expense_id] = expense
    return expense


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return None
