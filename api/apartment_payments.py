from flask import Blueprint, jsonify, request
from db_manager import connect
import json

# DB Connection
con = connect()
cursor = con.cursor()

# Define Blueprint
apartment_payments_bp = Blueprint('apartment_payments', __name__, url_prefix='/apartment_payments')


@apartment_payments_bp.route("/", methods=['GET'])
def payments():
    """ 
        A GET request that returns apartments payment information
        :param apartment_id - exact number of apartment id
        :param tenant_id - exact number of tenant id
        :return - JSON object that contains apartment payments information. The data returned is (payment_id, tenant_id, apartment_id, month, payment_date, amount)
    """
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
    """ 
        A POST request that adds a new apartment payment to the database.
        :param month - the month the tenant is paying for
        :param apartment_id - exact number of apartment id
        :param tenant_id - exact number of tenant id
        :param payment_date - the date the payment was made
        :param amount - payment amount
        :return - JSON object that contains the new payment id
    """
    # Get parameters from POST request
    data = request.get_json()
    apartment_id = data.get('apartment_id')
    month = data.get('month')
    tenant_id = data.get('tenant_id')
    payment_date = data.get('payment_date')
    amount = data.get('amount')

    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('ADD_PAYMENT_FUNC', int, [apartment_id, month,
                       tenant_id, payment_date, amount])
    con.commit()
    return jsonify(r)

@apartment_payments_bp.route('/invoice', methods=['GET'])
def get_invoice():
    """ 
        A GET request that creates a JSON object with the neccesary information to create an invoice.
        The invoice can be created by tenant_id and/or month that the tenant paid for.
        :param tenant_id - exact number of tenant id
        :param month - the month the tenant is paying for
        :return - JSON object that contains the new payment id
    """
    # Get p
    # Get parameters from GET request and add to dictionary
    tenant_id = request.args.get('tenant_id')
    month = request.args.get('month')   # Integer the represents the month; May = 5

    invoice_dict = {}
    invoice_dict['tenant_id'] = tenant_id
    invoice_dict['payments_details'] = {}
    
    if tenant_id and month:
        # Get all payments of the tenant in a specicifed month
        sql = f"SELECT * FROM apartment_payments WHERE tenant_id = {tenant_id}"
        cursor.execute(sql)
        r = cursor.fetchall()

        # Make a dictionary of payments and calculate committe percentage
        payments_dict = {}
        committe_payment = 0 

        i = 1
        for item in r:
            if item[3].month == int(month):
                payments_dict[i] = {}
                payments_dict[i]['payment_id'] = item[0]
                payments_dict[i]['apartment_id'] = item[2]
                payments_dict[i]['month'] = item[3].month
                payments_dict[i]['payment_date'] = item[4].strftime('%d-%m-%y')
                payments_dict[i]['amount'] = item[5]
                committe_payment += item[5]
                i += 1
        
        # Add payments_dict to the invoice_dict; with act as a nested dictionary
        invoice_dict['payments_details'] = payments_dict
        invoice_dict['committe_payment'] = committe_payment * 0.3

        return jsonify(invoice_dict)
    elif tenant_id:
        # Get parameters from GET request and add to dictionary
        tenant_id = request.args.get('tenant_id')

        invoice_dict = {}
        invoice_dict['tenant_id'] = tenant_id
        invoice_dict['payments_details'] = {}

        if tenant_id and month:
            # Get all payments of the tenant in a specicifed month
            sql = f"SELECT * FROM apartment_payments WHERE tenant_id = {tenant_id}"
            cursor.execute(sql)
            r = cursor.fetchall()

            # Make a dictionary of payments and calculate committe percentage
            payments_dict = {}
            committe_payment = 0

            i = 1
            for item in r:
                payments_dict[i] = {}
                payments_dict[i]['payment_id'] = item[0]
                payments_dict[i]['apartment_id'] = item[2]
                payments_dict[i]['month'] = item[3].month
                payments_dict[i]['payment_date'] = item[4].strftime('%d-%m-%y')
                payments_dict[i]['amount'] = item[5]
                committe_payment += item[5]
                i += 1
            
            # Add payments_dict to the invoice_dict; with act as a nested dictionary
            invoice_dict['payments_details'] = payments_dict
            invoice_dict['committe_payment'] = committe_payment * 0.3

            return jsonify(invoice_dict)
        
    else:
        msg = "The tenant_id and/or month fields must be sent as parameters."
        return jsonify(msg)
    
@apartment_payments_bp.route("/debts", methods=['GET'])
def debts():
    """ 
        A GET request that returns debts information about apartments payment
        :param apartment_id - exact number of apartment id
        :param tenant_id - exact number of tenant id
        :param month - number of month
        :param start_month - number of month
        :param end_month - number of month
        :return - JSON object that contains debts information about apartment payments .
    """
    # apartment_id = request.args.get('apartment_id')
    # tenant_id = request.args.get('tenant_id')
    month = request.args.get('month')
    start_month = request.args.get('start_month')
    end_month = request.args.get('end_month')

    
    debts_list = []
    if month:
        sql = """
            SELECT 
                at.apartment_id, 
                at.tenant_id,
                t.first_name || ' ' || t.last_name as full_name,
                at.rate
            FROM
                (SELECT debts.tenant_id
                FROM
                    (SELECT DISTINCT
                        ap.apartment_id, 
                        ap.tenant_id,
                        mp.monthly_sum,
                        (SELECT at.rate FROM apartment_tenants at WHERE at.tenant_id = ap.tenant_id) as rate
                    FROM 
                        apartment_payments ap,
                        (SELECT tenant_id, SUM(amount) monthly_sum
                        FROM apartment_payments 
                        WHERE EXTRACT(month FROM month) = :month
                        GROUP BY tenant_id) mp
                    WHERE ap.tenant_id = mp.tenant_id) debts
                WHERE debts.monthly_sum < debts.rate
                UNION
                (SELECT tenant_id
                FROM tenant
                MINUS
                SELECT count_payments.tenant_id
                FROM
                    (SELECT tenant_id, COUNT(payment_id) payments_amount
                    FROM apartment_payments
                    WHERE EXTRACT(month FROM month) = :month
                    GROUP BY tenant_id) count_payments)
                ) tenants_debts,
                apartment_tenants at,
                tenant t
            WHERE tenants_debts.tenant_id = at.tenant_id
            AND at.tenant_id = t.tenant_id
            """
        cursor.execute(sql, month)
        r = cursor.fetchall()
        v_month = int(month)
        i = 0
        for item in r:
            debts_list.append(list(item))
            tenant_debt = cursor.callfunc('TENANT_DEBT', int, [item[1], v_month])
            debts_list[i].append(tenant_debt)
            i += 1
        return jsonify(debts_list)
    
    if start_month and end_month:
        sql = """SELECT 
                    at.apartment_id, 
                    at.tenant_id,
                    t.first_name || ' ' || t.last_name as full_name,
                    at.rate
                FROM
                    (SELECT debts.tenant_id
                    FROM
                        (SELECT DISTINCT
                            ap.apartment_id, 
                            ap.tenant_id,
                            mp.monthly_sum,
                            (SELECT at.rate FROM apartment_tenants at WHERE at.tenant_id = ap.tenant_id) as rate
                        FROM 
                            apartment_payments ap,
                            (SELECT tenant_id, SUM(amount) monthly_sum
                            FROM apartment_payments 
                            WHERE EXTRACT(month FROM month) BETWEEN :start_month AND :end_month
                            GROUP BY tenant_id) mp
                        WHERE ap.tenant_id = mp.tenant_id) debts
                    WHERE debts.monthly_sum < debts.rate
                    UNION
                    (SELECT tenant_id
                    FROM tenant
                    MINUS
                    SELECT count_payments.tenant_id
                    FROM
                        (SELECT tenant_id, COUNT(payment_id) payments_amount
                        FROM apartment_payments
                        WHERE EXTRACT(month FROM month) BETWEEN :start_month AND :end_month
                        GROUP BY tenant_id) count_payments)
                    ) tenants_debts,
                    apartment_tenants at,
                    tenant t
                WHERE tenants_debts.tenant_id = at.tenant_id
                AND at.tenant_id = t.tenant_id"""
        cursor.execute(sql, [start_month, end_month])
        r = cursor.fetchall()
        v_start_month = int(start_month)
        v_end_month = int(end_month)
        tenant_debt = 0 
        i = 0
        for item in r:
            debts_list.append(list(item))
            for month in range(v_start_month, v_end_month + 1):
                tenant_debt += cursor.callfunc('TENANT_DEBT', int, [item[1], month])
            debts_list[i].append(tenant_debt)
            i += 1
        return jsonify(debts_list)