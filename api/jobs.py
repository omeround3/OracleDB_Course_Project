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
    job_id = request.args.get('id')
    if job_id:
        cursor.execute(f"SELECT * FROM JOBS WHERE TENANT_ID={job_id}")
        r = cursor.fetchall()
        con.commit()
        return jsonify(r)
    cursor.execute("select * from JOBS")
    r = cursor.fetchall()
    return jsonify(r)
