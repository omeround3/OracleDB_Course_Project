from flask import Blueprint, jsonify, request
from db_manager import connect

# DB Connection
con = connect()
cursor = con.cursor()

# Define Blueprint
apartment_payments_bp = Blueprint('apartment_payments', __name__, url_prefix='/apartment_payments')


@apartment_payments_bp.route("/", methods=['GET'])
def payments():
    apartment_id = request.args.get('apartment_id')
    tenant_id = request.args.get('tenant_id')
    if apartment_id and tenant_id:
        cursor.execute(
            f"SELECT * FROM apartment_payments WHERE apartment_id = {apartment_id} AND tenant_id = {tenant_id}")
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    elif tenant_id:
        cursor.execute(
            f"SELECT * FROM apartment_payments WHERE tenant_id = {tenant_id}")
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    elif apartment_id:
        cursor.execute(
            f"SELECT * FROM apartment_payments WHERE apartment_id = {apartment_id}")
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    cursor.execute("select * from apartment_payments")
    r = cursor.fetchall()
    return jsonify(r)

@apartment_payments_bp.route('/add', methods=['POST'])
def add_payment():
    # Get parameters from POST request
    apartment_id = request.form.get('apartment_id')
    month = request.form.get('month')
    tenant_id = request.form.get('tenant_id')
    payment_date = request.form.get('payment_date')
    amount = request.form.get('amount')

    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('ADD_PAYMENT_FUNC', int, [apartment_id, month,
                       tenant_id, payment_date, amount])
    con.commit()
    return jsonify(r)