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
    # Get parameters from GET request
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
    job_types = ('cleaning', 'horticulture',
                 'plumbing', 'renovation', 'security')
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
    # Get parameters from GET request
    job_id = request.args.get('job_id')

    # Call DELETE_JOB_PROC from DB
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
    # Get parameters from GET request
    contractor_id = request.args.get('contractor_id')
    job_id = request.args.get('job_id')

    # Define SQL statement
    sql = """
            SELECT 
                jb.job_id, 
                jb.contractor_id, 
                c.contractor_name,
                jb.price
            FROM jobs_bids jb, contractors c
            WHERE jb.contractor_id = c.contractor_id
            """

    if contractor_id and job_id:
        contractor_job_sql = sql + """ AND jb.contractor_id = :contractor_id
                                    AND jb.job_id = :job_id"""
        cursor.execute(contractor_job_sql, [contractor_id, job_id])
        r = cursor.fetchall()
        return jsonify(r)
    elif contractor_id:
        contractor_id_sql = sql + """ AND jb.contractor_id = :contractor_id"""
        cursor.execute(contractor_id_sql, [contractor_id])
        r = cursor.fetchall()
        return jsonify(r)
    elif job_id:
        job_id_sql = sql + """ AND jb.job_id = :job_id"""
        cursor.execute(job_id_sql, [job_id])
        r = cursor.fetchall()
        return jsonify(r)
    else:
        cursor.execute(sql)
        r = cursor.fetchall()
        return jsonify(r)


@jobs_bp.route('/show-payments', methods=['GET'])
def show_payments():
    """ 
        A GET request to show jobs payment information.
        :param contractor_id - exact number of contractor id
        :param contractor_name - exact number of contractor id
        :param job_id - exact number of job id
        :param job_type - search payments by job type
        :param month - search payments by month
        :return - JSON object that contains jobs bids information.
    """
    # Get parameters from GET request
    contractor_id = request.args.get('contractor_id')
    contractor_name = request.args.get('contractor_name')
    job_id = request.args.get('job_id')
    job_type = request.args.get('job_type')
    month = request.args.get('month')

    # Define SQL statement
    sql = """
                SELECT cp.*, j.job_type, c.contractor_name
                FROM contractors_payments cp, jobs j, jobs_bids jb, contractors c
                WHERE cp.job_id = jb.job_id
                AND cp.job_id = j.job_id
                AND jb.contractor_id = c.contractor_id
                """
    
    # Integrity check
    job_types = ('cleaning', 'horticulture',
                 'plumbing', 'renovation', 'security')
    if job_type:
        if job_type not in job_types:
            return f'Job type is invaild. The available jobs types are: {job_types}'
        elif month:
            job_type_sql = sql + """ AND j.job_type = :job_type
                                     AND EXTRACT(month FROM payment_date) = :month"""
            cursor.execute(job_type_sql, [job_type, month])
            r = cursor.fetchall()
            return jsonify(r)
        else:
            job_type_sql = sql + """ AND j.job_type = :job_type"""
            cursor.execute(job_type_sql, [job_type])
            r = cursor.fetchall()
            return jsonify(r)

    elif contractor_id:
        if month:
            contractor_id_sql = sql + """ AND c.contractor_id = :contractor_id
                                          AND EXTRACT(month FROM payment_date) = :month"""
            cursor.execute(contractor_id_sql, [contractor_id, month])
            r = cursor.fetchall()
            return jsonify(r)
        else:
            contractor_id_sql = sql + """ AND c.contractor_id = :contractor_id"""
            cursor.execute(contractor_id_sql, [contractor_id])
            r = cursor.fetchall()
            return jsonify(r)
    elif contractor_name:
        if month:
            contractor_name_sql = sql + """ AND c.contractor_name LIKE :contractor_name || '%' 
                                            AND EXTRACT(month FROM payment_date) = :month"""
            cursor.execute(contractor_name_sql, [contractor_name, month])
            r = cursor.fetchall()
            return jsonify(r)
        else:
            contractor_name_sql = sql + """ AND c.contractor_name LIKE :contractor_name || '%'"""
            cursor.execute(contractor_name_sql, [contractor_name])
            r = cursor.fetchall()
            return jsonify(r)
    elif job_id:
        if month:
            job_sql = sql + """ AND cp.job_id = :job_id
                          AND EXTRACT(month FROM payment_date) = :month"""
            cursor.execute(job_sql, [job_id, month])
            r = cursor.fetchall()
            return jsonify(r)
        else:
            job_sql = sql + """ AND cp.job_id = :job_id"""
            cursor.execute(job_sql, [job_id])
            r = cursor.fetchall()
            return jsonify(r)
    elif month:
        month = int(month)
        month_sql = sql + """ AND EXTRACT(month FROM payment_date) = :month"""
        cursor.execute(month_sql, [month])
        r = cursor.fetchall()
        return jsonify(r)
    else:
        cursor.execute(sql)
        r = cursor.fetchall()
        return jsonify(r)


@jobs_bp.route('/add-payment', methods=['POST'])
def add_payment():
    """ 
        A POST request that adds a new job payment to the database.
        :param job_id - exact number of job id
        :param payment_date - the date the payment was made
        :param price - payment amount
        :param payment_description - A description for the payment - NULLABLE
        :return - JSON object that contains the new payment id
    """
    # Get parameters from POST request
    data = request.get_json()
    job_id = data.get('job_id')
    payment_date = data.get('payment_date')
    price = data.get('price')
    payment_description = data.get('payment_description')

    # Call ADD_JOB_PAYMENT from DB
    r = cursor.callfunc('ADD_JOB_PAYMENT', int, [
                        job_id, payment_date, price, payment_description])
    con.commit()
    return jsonify(r)


@jobs_bp.route('/gets-plans', methods=['GET'])
def get_plans():
    """ 
        A GET request that gets all the information about maintenance plans.
        :param plan_id - look up plans by plan id
        :param job_id - look up plans by job id
        :param contractor_id - look up plans by contractor id
        :param status - get plans by status options are ( 'approved', 'declined', 'waiting' ) 
        :return - JSON object that contains maintenance plans information. Columns order: (plan_id, status, description, job_type, contractor_name)
    """

    # Get parameters from GET request
    plan_id = request.args.get('plan_id')
    job_id = request.args.get('job_id')
    contractor_id = request.args.get('contractor_id')
    status = request.args.get('status')

    status_types = ('approved', 'declined', 'waiting')

    
    sql = """
            SELECT mp.*, j.job_type, c.contractor_name
            FROM maintenance_plan mp
            INNER JOIN jobs_plans jp
            ON mp.plan_id = jp.plan_id
            INNER JOIN jobs j
            ON jp.job_id = j.job_id
            INNER JOIN jobs_bids jb
            ON jb.job_id = j.job_id
            INNER JOIN contractors c
            ON jb.contractor_id = c.contractor_id
        """
    if status:
        if status not in status_types:
            return f'Status type is invaild. The available status types are: {status_types }'

        status_sql = sql + """ WHERE mp.status = :status"""
        cursor.execute(status_sql, [status])
        r = cursor.fetchall()
        return jsonify(r)

    elif plan_id:
        plan_sql = sql + """ WHERE mp.plan_id = :plan_id"""
        cursor.execute(plan_sql, [plan_id])
        r = cursor.fetchall()
        return jsonify(r)
        
    elif job_id:
        job_sql = sql + """ WHERE jp.job_id = :job_id"""
        cursor.execute(job_sql, [job_id])
        r = cursor.fetchall()
        return jsonify(r)
        
    elif contractor_id:
        contractor_sql = sql + """ WHERE jb.contractor_id = :contractor_id"""
        cursor.execute(contractor_sql, [contractor_id])
        r = cursor.fetchall()
        return jsonify(r)
    else:
        cursor.execute(sql)
        r = cursor.fetchall()
        return jsonify(r)
