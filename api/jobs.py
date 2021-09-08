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
        A GET request that returns jobs information
        :param id - exact number of job id
        :return - JSON object that contains jobs information
    """
    job_id = request.args.get('job_id')
    if job_id:
        sql = """
                SELECT 
                    j.job_id, 
                    j.job_type, 
                    j.description, 
                    t.first_name || ' ' || t.last_name as tenant_name
                FROM jobs j, tenant t
                WHERE j.tenant_id = t.tenant_id
                AND job_id = :job_id
              """
        cursor.execute(sql, [job_id])
        r = cursor.fetchall()
        return jsonify(r)
    sql = """
            SELECT 
                j.job_id, 
                j.job_type, 
                j.description, 
                t.first_name || ' ' || t.last_name as tenant_name
            FROM jobs j, tenant t
            WHERE j.tenant_id = t.tenant_id
            """
    cursor.execute(sql)
    r = cursor.fetchall()
    return jsonify(r)

@jobs_bp.route('/request-job', methods=['POST'])
def request_job():
    """ 
        A POST request that adds a job request from a tenant
        :param job_type - the month the tenant is paying for
        :param tenant_id - exact number of tenant id
        :param description - description of job - NULLABLE
        :return - JSON object that contains the new job id
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

@jobs_bp.route('/delete', methods=['GET'])
def delete_job():
    """ 
        A GET request to delete a job by job id
        :param job_id - exact number of job id
        :return - the deleted job id
    """
    # Get parameters from POST request
    job_id = request.args.get('job_id')

    # Call DELETE_TENANT_PROC from DB
    r = cursor.callproc('DELETE_JOB_PROC', [job_id])
    con.commit()
    return jsonify(r)

@jobs_bp.route('/bids', methods=['GET'])
def get_bids():
    """ 
        A GET request to show jobs bids information, which is basically just the bids of contractors for different kinds of jobs.
        :param contractor_id - exact number of contractor id
        :param job_id - exact number of job id
        :return - JSON object that contains jobs bids information.
    """
    contractor_id = request.args.get('contractor_id')
    job_id = request.args.get('job_id')

    # if contractor_id and job_id:
        
    # elif contractor_id:
    
    # elif job_id:

    # else: