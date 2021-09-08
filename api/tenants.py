from flask import Blueprint, jsonify, request
from db_manager import connect

# DB Connection
con = connect()
cursor = con.cursor()

# Define Blueprint
tenants_bp = Blueprint('tenants', __name__, url_prefix='/tenants')


@tenants_bp.route("/", methods=['GET'])
def tenants():
    name = request.args.get('name')
    tenant_id = request.args.get('id')
    if name:
        sql = """SELECT 
                    t.tenant_id, 
                    t.first_name, 
                    t.last_name, 
                    t.age,
                    t.phone,
                    at.apartment_id,
                    at.rate,
                    at.last_vote_date
                FROM tenant t
                RIGHT JOIN apartment_tenants at ON t.tenant_id = at.tenant_id
                WHERE FIRST_NAME LIKE :name or LAST_NAME like :name"""
        cursor.execute(sql, [name, name])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    elif tenant_id:
        sql = """SELECT 
                    t.tenant_id, 
                    t.first_name, 
                    t.last_name, 
                    t.age,
                    t.phone,
                    at.apartment_id,
                    at.rate,
                    at.last_vote_date
                FROM tenant t
                RIGHT JOIN apartment_tenants at ON t.tenant_id = at.tenant_id
                WHERE t.tenant_id = :tenant_id"""
        cursor.execute(sql, [tenant_id])
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    else:
        sql = """SELECT 
                    t.tenant_id, 
                    t.first_name, 
                    t.last_name, 
                    t.age,
                    t.phone,
                    at.apartment_id,
                    at.rate,
                    at.last_vote_date
                FROM tenant t
                RIGHT JOIN apartment_tenants at ON t.tenant_id = at.tenant_id"""
        cursor.execute(sql)
        r = cursor.fetchall()
        return jsonify(r)


@tenants_bp.route('/add', methods=['POST'])
def add_tenant():
    # Get parameters from POST request
    tenant_id = request.form.get('tenant_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    phone = request.form.get('phone')
    apartment_id = request.form.get('apartment_id')
    rate = request.form.get('rate')
    last_vote_date = request.form.get('last_vote_date', None)

    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('ADD_TENANT_FUNC', int, [tenant_id, first_name,
                                                 last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)


@tenants_bp.route('/update', methods=['POST'])
def update_tenant():
    # Get parameters from POST request
    tenant_id = request.form.get('tenant_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    phone = request.form.get('phone')
    apartment_id = request.form.get('apartment_id')
    rate = request.form.get('rate')
    last_vote_date = request.form.get('last_vote_date')

    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('UPDATE_TENANT_FUNC', int, [tenant_id, first_name,
                                                    last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)

@tenants_bp.route('/available-apartments', methods=['GET'])
def available_apartments():
    """ Returns a list of available apartments (not fully occupied) """
    sql = "SELECT apartment_id FROM apartment"
    cursor.execute(sql)
    apartments_id = cursor.fetchall()
    available_apartments = []

    # Filter fully occupied apartments
    for id in apartments_id:
        if (cursor.callfunc('IS_APARTMENT_FULL', bool, id) == False):
            available_apartments.append(id)
    
    return jsonify(available_apartments)

@tenants_bp.route('/delete', methods=['GET'])
def delete_tenant():
    # Get parameters from POST request
    tenant_id = request.args.get('id')

    # Call DELETE_TENANT_PROC from DB
    r = cursor.callproc('DELETE_TENANT_PROC', [tenant_id])
    con.commit()
    return jsonify(r)
    


