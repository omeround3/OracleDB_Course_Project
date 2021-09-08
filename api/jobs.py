from flask import Blueprint, jsonify, request
from db_manager import connect, output_type_handler

# DB Connection
con = connect()
con.outputtypehandler = output_type_handler
cursor = con.cursor()


# Define Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')


@jobs_bp.route("/", methods=['GET'])
def jobs():
    """ 
        A GET request that returns apartments payment information
        :param id - exact number of job id
        :return - JSON object that contains apartment payments information
    """
    job_id = request.args.get('id')
    if job_id:
        sql = """SELECT * FROM jobs WHERE job_id = :job_id"""
        cursor.execute(sql, [job_id])
        r = cursor.fetchall()
        return jsonify(r)
    cursor.execute("SELECT * FROM jobs")
    r = cursor.fetchall()
    return jsonify(r)

@jobs_bp.route('/request-job', methods=['POST'])
def request_job():
    """ 
        A POST request that adds a job request from a tenant
        :param job_type - the month the tenant is paying for
        :param tenant_id - exact number of tenant id
        :param description - description of job - NULLABLE
        :return - JSON object that contains the new payment id
    """
    # Get parameters from POST request
    data = request.get_json()
    job_type = data.get('job_type')
    tenant_id = data.get('tenant_id')
    description = data.get('description')
    
    # Integrity check
    job_types = ( 'cleaning', 'horticulture', 'plumbing', 'renovation', 'security' )
    if job_type not in job_types:
        return f'Job type is invaild. The available jobs types are: {job_types}'

    # Call ADD_JOB_FUNC from DB
    r = cursor.callfunc('ADD_JOB_FUNC', int, [job_type,
        tenant_id, description])
    con.commit()
    return jsonify(r)