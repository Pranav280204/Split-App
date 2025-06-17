Split App Backend
Backend for splitting group expenses, built with Flask and SQLite (local) or PostgreSQL (deployed).
Setup (Local)

Clone: git clone <your-repo-url>
Install: pip install -r requirements.txt
Run: python app.py

API Endpoints

GET /expenses: List all expenses
POST /expenses: Add expense (amount, description, paid_by)
PUT /expenses/:id: Update expense
DELETE /expenses/:id: Delete expense
GET /people: List all people
GET /balances: Show balances (owes/owed)
GET /settlements: Get optimized settlements

Deployment

Hosted on Railway: <your-railway-url> (update after deployment)
Postman Collection: <your-gist-url> (update after creating)

Settlement Logic

Balances: total_spent_by_person - (total_expenses / num_people)
Settlements: Minimize transactions by matching debtors to creditors
Amounts rounded to 2 decimal places

Limitations

Assumes equal splits for expenses
No support for percentage/exact amount splits
No optional features (e.g., categories, recurring expenses)

