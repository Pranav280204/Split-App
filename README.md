# Split App Backend

## Overview
A backend for splitting expenses among groups, with expense tracking and settlement calculations.

## Setup (Local)
1. Clone repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python app.py`

## API Endpoints
- `GET /expenses`: List all expenses.
- `POST /expenses`: Add expense (fields: amount, description, paid_by).
- `PUT /expenses/:id`: Update expense.
- `DELETE /expenses/:id`: Delete expense.
- `GET /people`: List all people.
- `GET /balances`: Show balances (owes/owed).
- `GET /settlements`: Get optimized settlement transactions.

## Deployment
- Hosted on Railway.app: `<deployed-url>`
- Postman Collection: `<gist-url>`

## Settlement Logic
- Balances: `total_spent_by_person - (total_expenses / num_people)`.
- Settlements: Match debtors to creditors to minimize transactions.

## Limitations
- Assumes equal splits for simplicity.
- No support for percentage/exact amount splits (optional feature omitted).
