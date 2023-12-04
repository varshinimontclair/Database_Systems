
from flask import Flask, render_template,request, redirect, jsonify,session
from decimal import Decimal
import pymysql



app = Flask(__name__)


# Database configuration

db = pymysql.connect(host="127.0.0.1", user="root", password="varshuadmin", database="llc_tax_payment_system",cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

# Routes
@app.route('/')
def index():
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM TaxBreakDown')
        tax = cursor.fetchall()
    return render_template('index.html', tax=tax)

@app.route('/save', methods=['POST'])
def save():
    try:
        # Get data from the form
        Company = request.form['Company']
        Amount = request.form['Amount']
        PaymentDate = request.form['PaymentDate']
        Status = request.form['Status']
        DueDate = request.form['DueDate']

        # Insert the new record into the TaxBreakDown table
        with db.cursor() as cursor:
            cursor.execute('INSERT INTO TaxBreakDown (Company, Amount, PaymentDate, Status, DueDate) VALUES (%s, %s, %s, %s, %s)',
                           (Company, Amount, PaymentDate, Status, DueDate))
            db.commit()

        return redirect('/')
    except Exception as e:
        # Handle exceptions (e.g., log the error)
        print(f"An error occurred: {e}")
        db.rollback()  # Rollback the transaction to avoid leaving incomplete data

        return "Error occurred", 500  # Return an HTTP 500 Internal Server Error response
    return redirect('/')

# Endpoint for deleting a record
@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    with db.cursor() as cursor:
        cursor.execute('DELETE FROM TaxBreakDown WHERE Id = %s', (record_id,))
        db.commit()
    return redirect('/')

@app.route('/update', methods=['POST'])
def update_record():
    try:
        # Parse JSON data from the request
        data = request.json
        row_id = data['rowId']
        column_name = data['columnName']
        updated_value = data['updatedValue']

        # Update the record in the TaxBreakDown table
        with db.cursor() as cursor:
            cursor.execute(f'UPDATE TaxBreakDown SET {column_name} = %s WHERE Id = %s', (updated_value, row_id))
            db.commit()

        return jsonify({'success': True, 'message': 'Record updated successfully'})
    except Exception as e:
        # Handle exceptions (e.g., log the error)
        print(f"An error occurred: {e}")
        db.rollback()  # Rollback the transaction to avoid leaving incomplete data

        return jsonify({'success': False, 'message': 'Error occurred while updating the record'})
    return redirect('/')

# Add this route to your Flask app
@app.route('/filter', methods=['POST'])
def filter_data():
    due_date_filter = request.form.get('dueDateFilter')
    tax_Rate = request.form.get('taxRate')
    # Convert tax_Rate to a decimal.Decimal object
    tax_Rate_decimal = Decimal(tax_Rate) if tax_Rate else Decimal(0)
    # Construct your SQL query based on the filter
    if due_date_filter:
        query = f"SELECT * FROM TaxBreakDown WHERE DueDate = '{due_date_filter}'"
        total = f"SELECT SUM(CAST(REPLACE(Amount, ',', '') AS DECIMAL(10, 2))) AS Amount FROM TaxBreakDown WHERE DueDate = '{due_date_filter}'"
    else:
        query = "SELECT * FROM TaxBreakDown"

    cursor.execute(query)
    filtered_data = cursor.fetchall()
    cursor.execute(total)
    result = cursor.fetchone()
    total_sum = result['Amount'] if result and result.get('Amount') is not None else 0


    tax_due = total_sum * tax_Rate_decimal 
    formatted_tax_due = '{:.2f}'.format(tax_due).rstrip('0').rstrip('.')
    tax_Rate = int(tax_Rate_decimal * 100)


    return render_template('/taxtable.html', filtered_data=filtered_data, total_sum=total_sum,tax_Rate = tax_Rate,tax_due = formatted_tax_due)




@app.route('/tax/all')
def tax():
    cursor.execute("SELECT * FROM TaxBreakDown")
    tax = cursor.fetchall()
    return render_template('index.html', tax=tax)

if __name__ == '__main__':
    app.run(debug=True)