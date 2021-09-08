from flask import Blueprint, jsonify, request
from db_manager import connect

# DB Connection
con = connect()
cursor = con.cursor()

# Define Blueprint
tenants_bp = Blueprint('tenants', __name__, url_prefix='/tenants')


@tenants_bp.route("/", methods=['GET'])
def tenants():
    """ 
        A GET request that returns tenants information.
        :param name - a name of the tenant. This will return names that begins with the input string
        :param tenant_id - exact number of tenant id
        :return - JSON object
    """
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
                WHERE FIRST_NAME LIKE :name || '%' or LAST_NAME like :name || '%'"""
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
    """ 
        A function to add a new tenant 
        :param tenant_id - exact number of tenant id
        :param first_name - tenant first_name
        :param last_name - tenant last_name
        :param age - tenant age
        :param phone - tenant phone number
        :param rate - tenant rate
        :param last_vote_date - last vote date for the committe - NULLABLE
        :return - JSON object that contains tenant_id
    """
    # Get parameters from POST request
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    phone = data.get('phone')
    apartment_id = data.get('apartment_id')
    rate = data.get('rate')
    last_vote_date = request.form.get('last_vote_date', None)
    print(f"{tenant_id=}, {apartment_id=} , {last_vote_date=}")
    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('ADD_TENANT_FUNC', int, [tenant_id, first_name,
                                                 last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)


@tenants_bp.route('/update', methods=['POST'])
def update_tenant():
    """ 
        A POST request to update the tenant details
        :param tenant_id - exact number of tenant id
        :param first_name - tenant first_name
        :param last_name - tenant last_name
        :param age - tenant age
        :param phone - tenant phone number
        :param rate - tenant rate
        :param last_vote_date - last vote date for the committe - NULLABLE
        :return - JSON object that contains tenant_id
    """
    # Get parameters from POST request
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    phone = data.get('phone')
    apartment_id = data.get('apartment_id')
    rate = data.get('rate')
    last_vote_date = request.form.get('last_vote_date', None)

    # Call UPDATE_TENANT_FUNC from DB
    r = cursor.callfunc('UPDATE_TENANT_FUNC', int, [tenant_id, first_name,
                                                    last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)

@tenants_bp.route('/available-apartments', methods=['GET'])
def available_apartments():
    """ 
        Returns a list of available apartments (not fully occupied) 
        :return - JSON object that contains list of available apartments
    """
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
    """ 
        A GET request to delete a tenant by tenant id
        :param tenant_id - exact number of tenant id
        :return - JSON object that contains list of available apartments
    """
    # Get parameters from GET request
    tenant_id = request.args.get('id')

    # Call DELETE_TENANT_PROC from DB
    r = cursor.callproc('DELETE_TENANT_PROC', [tenant_id])
    con.commit()
    return jsonify(r)
    


