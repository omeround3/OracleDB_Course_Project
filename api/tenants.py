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
    if name:
        cursor.execute(
            f"SELECT * FROM tenant WHERE FIRST_NAME LIKE '{name}%' or LAST_NAME like '{name}%'")
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    cursor.execute("select * from tenant")
    r = cursor.fetchall()
    con.commit()
    return jsonify(r)


@tenants_bp.route('/add', methods=['POST'])
def add_tenant():
    # Get parameters from POST request
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    phone = request.form.get('phone')
    apartment_id = request.form.get('apartment_id')
    rate = request.form.get('rate')
    last_vote_date = request.form.get('last_vote_date')

    # Call ADD_TENANT_FUNC from DB
    # obj_type = connection.gettype("NUMBER")
    r = cursor.callfunc('ADD_TENANT_FUNC', int, [id, first_name,
                                                 last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)


@tenants_bp.route('/update', methods=['POST'])
def update_tenant():
    # Get parameters from POST request
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    phone = request.form.get('phone')
    apartment_id = request.form.get('apartment_id')
    rate = request.form.get('rate')
    last_vote_date = request.form.get('last_vote_date')

    # Call ADD_TENANT_FUNC from DB
    r = cursor.callfunc('UPDATE_TENANT_FUNC', int, [id, first_name,
                                                    last_name, age, phone, apartment_id, rate, last_vote_date])
    con.commit()
    return jsonify(r)
