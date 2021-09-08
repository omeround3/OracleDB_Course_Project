from flask import Blueprint, jsonify, request
from db_manager import connect

# DB Connection
con = connect()
cursor = con.cursor()

# Define Blueprint
apartment_bp = Blueprint('apartments', __name__, url_prefix='/apartments')


@apartment_bp.route('/', methods=['GET'])
def aparments():
    apartment_id = request.args.get('apartment_id')

    if apartment_id:
        sql = """SELECT * FROM apartment WHERE apartment_id = :apartment_id"""
        cursor.execute(sql, [apartment_id])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    else:
        sql = """SELECT * FROM apartment"""
        cursor.execute(sql)
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)


@apartment_bp.route('/occupancy', methods=['GET'])
def aparments_occupancy():
    apartment_id = request.args.get('apartment_id')
    ordered = request.args.get('ordered')    # ordered = 1 is considered ordered

    if apartment_id:
        sql = """SELECT 
                    apartment_id, 
                    current_number_tenants,
                    max_number_tenants,
                    CASE
                        WHEN max_number_tenants - current_number_tenants > 0 THEN 'Not Full'
                        ELSE 'Full'
                    END AS status
                FROM apartment_occupancy
                WHERE apartment_id = :apartment_id"""
        cursor.execute(sql, [apartment_id])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    elif ordered:
        sql = """SELECT 
                    apartment_id, 
                    current_number_tenants,
                    max_number_tenants,
                    CASE
                        WHEN max_number_tenants - current_number_tenants > 0 THEN 'Not Full'
                        ELSE 'Full'
                    END AS status
                FROM apartment_occupancy
                ORDER BY status DESC"""
        cursor.execute(sql)
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    else:
        sql = """SELECT 
                    apartment_id, 
                    current_number_tenants,
                    max_number_tenants,
                    CASE
                        WHEN max_number_tenants - current_number_tenants > 0 THEN 'Not Full'
                        ELSE 'Full'
                    END AS status
                FROM apartment_occupancy"""
        cursor.execute(sql)
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)


@apartment_bp.route('/total-rates', methods=['GET'])
def aparments_total_rate():
    apartment_id = request.args.get('apartment_id')

    if apartment_id:
        sql = """SELECT * FROM apartments_total_rates WHERE apartment_id = :apartment_id"""
        cursor.execute(sql, [apartment_id])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    else:
        sql = """SELECT * FROM apartments_total_rates"""
        cursor.execute(sql)
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)


@apartment_bp.route('/tenants', methods=['GET'])
def apartment_tenants():
    apartment_id = request.args.get('apartment_id')

    if apartment_id:
        sql = """SELECT 
                    t.first_name,
                    t.last_name,
                    at.rate
                FROM tenant t 
                JOIN apartment_tenants at ON t.tenant_id = at.tenant_id
                WHERE at.apartment_id = :apartment_id"""
        cursor.execute(sql, [apartment_id])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    else:
        return 'An apartment ID must be specicifed'
