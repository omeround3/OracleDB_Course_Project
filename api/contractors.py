from flask import Blueprint, jsonify, request
from db_manager import connect, output_type_handler

# DB Connection
con = connect()
cursor = con.cursor()


# Define Blueprint
contractors_bp = Blueprint('contractors', __name__, url_prefix='/contractors')


@contractors_bp.route("/", methods=['GET'])
def contractors():
    """ 
        A GET request that returns contractors information
        :param contractor_id - exact number of contractor id
        :param contractor_name - Search by contractor name
        :return - JSON object that contains contractors information
    """
    contractor_id = request.args.get('contractor_id')
    contractor_name = request.args.get('contractor_name')
    if contractor_id and contractor_name:
        sql = """
                SELECT 
                    c.contractor_id, 
                    c.contractor_name, 
                    c.address
                FROM contractors c
                WHERE contractor_name LIKE :contractor_name || '%'
                AND c.contractor_id = :contractor_id
              """
        cursor.execute(sql, [contractor_name, contractor_id])
        r = cursor.fetchall()
        return jsonify(r)
    elif contractor_name:
        sql = """
                SELECT 
                    c.contractor_id, 
                    c.contractor_name, 
                    c.address
                FROM contractors c
                WHERE contractor_name LIKE :contractor_name || '%'
              """
        cursor.execute(sql, [contractor_name])
        r = cursor.fetchall()
        return jsonify(r)
    elif contractor_id:
        sql = """
                SELECT 
                    c.contractor_id, 
                    c.contractor_name, 
                    c.address
                FROM contractors c
                WHERE c.contractor_id = :contractor_id
              """
        cursor.execute(sql, [contractor_id])
        r = cursor.fetchall()
        return jsonify(r)
    sql = """
            SELECT 
                c.contractor_id, 
                c.contractor_name, 
                c.address
            FROM contractors c
            """
    cursor.execute(sql)
    r = cursor.fetchall()
    return jsonify(r)

@contractors_bp.route('/add', methods=['POST'])
def add_contractor():
    """ 
        A POST request that adds a contractor to the system
        :param contractor_id - exact contractor id
        :param contractor_name - the month the tenant is paying for
        :param address - address of the contractor - NULLABLKE
        :return - JSON object that contains the new contractor id
    """
    # Get parameters from POST request
    data = request.get_json()
    contractor_id = data.get('contractor_id')
    contractor_name = data.get('contractor_name')
    address = data.get('address')
    
    # Call ADD_JOB_FUNC from DB
    r = cursor.callfunc('ADD_CONTRACTOR_FUNC', int, [contractor_id, contractor_name, address])
    con.commit()
    return jsonify(r)

@contractors_bp.route('/delete', methods=['GET'])
def delete_contractor():
    """ 
        A GET request to delete a contractor by contractor id
        :param contractor_ID - exact number of job id
        :return - the deleted job id
    """
    # Get parameters from POST request
    contractor_id = request.args.get('contractor_id')

    # Call DELETE_TENANT_PROC from DB
    r = cursor.callproc('DELETE_CONTRACTOR_PROC', [contractor_id])
    con.commit()
    return jsonify(r)