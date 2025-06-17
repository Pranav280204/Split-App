from flask import Flask, request, jsonify
from models import db, Expense, Person
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

# Helper: Validate input
def validate_expense(data):
    if not all(key in data for key in ['amount', 'description', 'paid_by']):
        return False, "Missing required fields"
    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return False, "Amount must be positive"
    if not data['description'].strip():
        return False, "Description cannot be empty"
    if not data['paid_by'].strip():
        return False, "Paid_by cannot be empty"
    return True, ""

# GET /expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify({
        'success': True,
        'data': [{'id': e.id, 'amount': e.amount, 'description': e.description, 'paid_by': e.paid_by} for e in expenses]
    }), 200

# POST /expenses
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    valid, error = validate_expense(data)
    if not valid:
        return jsonify({'success': False, 'message': error}), 400
    
    expense = Expense(amount=data['amount'], description=data['description'], paid_by=data['paid_by'])
    db.session.add(expense)
    
    # Add person if not exists
    if not Person.query.get(data['paid_by']):
        db.session.add(Person(name=data['paid_by']))
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Expense added successfully', 'data': data}), 201

# PUT /expenses/:id
@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'success': False, 'message': 'Expense not found'}), 404
    
    data = request.get_json()
    valid, error = validate_expense(data)
    if not valid:
        return jsonify({'success': False, 'message': error}), 400
    
    expense.amount = data['amount']
    expense.description = data['description']
    expense.paid_by = data['paid_by']
    
    if not Person.query.get(data['paid_by']):
        db.session.add(Person(name=data['paid_by']))
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Expense updated successfully'}), 200

# DELETE /expenses/:id
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'success': False, 'message': 'Expense not found'}), 404
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Expense deleted successfully'}), 200

# GET /people
@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    return jsonify({
        'success': True,
        'data': [p.name for p in people]
    }), 200

# GET /balances
@app.route('/balances', methods=['GET'])
def get_balances():
    expenses = Expense.query.all()
    people = Person.query.all()
    if not people:
        return jsonify({'success': True, 'data': {}, 'message': 'No expenses or people'}), 200
    
    balances = {p.name: 0 for p in people}
    total_spent = sum(e.amount for e in expenses)
    fair_share = total_spent / len(people) if people else 0
    
    for expense in expenses:
        balances[expense.paid_by] += expense.amount
    
    for person in balances:
        balances[person] -= fair_share  # Positive: owed, Negative: owes
    
    return jsonify({'success': True, 'data': balances}), 200

# GET /settlements
@app.route('/settlements', methods=['GET'])
def get_settlements():
    balances = get_balances().get_json()['data']
    if not balances:
        return jsonify({'success': True, 'data': [], 'message': 'No settlements needed'}), 200
    
    settlements = []
    debtors = [(name, bal) for name, bal in balances.items() if bal < -0.01]
    creditors = [(name, bal) for name, bal in balances.items() if bal > 0.01]
    
    for debtor, debt in debtors:
        debt = -debt
        for creditor, credit in creditors:
            if debt <= 0:
                break
            amount = min(debt, credit)
            if amount > 0:
                settlements.append({
                    'from': debtor,
                    'to': creditor,
                    'amount': round(amount, 2)
                })
                debt -= amount
                for c in creditors:
                    if c[0] == creditor:
                        c[1] -= amount
                        break
    
    return jsonify({'success': True, 'data': settlements}), 200

if __name__ == '__main__':
    app.run(debug=True)
