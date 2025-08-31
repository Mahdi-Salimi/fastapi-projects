from fastapi import FastAPI, HTTPException, status
from typing import Dict

app = FastAPI(title="Expense Manager API")

expenses: Dict[int, dict] = {}
next_id: int = 1 

@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(data: dict):
    global next_id

    description = data.get("description")
    amount = data.get("amount")

    if description is None or amount is None:
        raise HTTPException(status_code=400, detail="description and amount are required")

    expense = {"id": next_id, "description": description, "amount": float(amount)}
    expenses[next_id] = expense
    next_id += 1
    return expense


@app.get("/expenses")
def get_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, data: dict):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    description = data.get("description")
    amount = data.get("amount")

    if description is None or amount is None:
        raise HTTPException(status_code=400, detail="description and amount are required")

    expenses[expense_id] = {"id": expense_id, "description": description, "amount": float(amount)}
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
    return None