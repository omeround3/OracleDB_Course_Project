from flask import Blueprint, jsonify, request
from db_manager import connect, output_type_handler

# DB Connection
con = connect()
cursor = con.cursor()


# Define Blueprint
statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_bp.route("/", methods=['GET'])
def statistics():
    """ 
        A GET request that returns statistics about the committe system.
        Specifically, the number of apartments, number of not fully occupied apartments, number of tenants, number of approved plans, number of declined plans, number of waiting for approval plans, committe balance.
        :return - JSON object that contains statistics information
    """

    r = {}
    # Get number of apartments
    cursor.execute("SELECT COUNT(apartment_id) FROM apartment")
    num_apartments = cursor.fetchall()
    r['num_apartments'] = num_apartments[0][0]
    
    # Get number of not fully occupied apartments
    cursor.execute("""SELECT COUNT(apartment_id) 
                    FROM apartment_occupancy ao
                    WHERE DECODE(ao.max_number_tenants - ao.current_number_tenants, 0 , 'FULL', 'NOT FULL') = 'NOT FULL'""")
    num_not_full_apartments = cursor.fetchall()
    r['num_not_full_apartments'] = num_not_full_apartments[0][0]

    # Get number of not fully occupied apartments
    cursor.execute("SELECT COUNT(tenant_id) FROM tenant")
    num_tenants = cursor.fetchall()
    r['num_tenants'] = num_tenants[0][0]

    # Get number of approved maintenance plans
    cursor.execute("""SELECT COUNT(plan_id) 
                    FROM maintenance_plan
                    WHERE status = 'approved'""")
    num_approved_plans = cursor.fetchall()
    r['num_approved_plans'] = num_approved_plans[0][0]

    # Get number of declined maintenance plans
    cursor.execute("""SELECT COUNT(plan_id) 
                    FROM maintenance_plan
                    WHERE status = 'declined'""")
    num_declined_plans = cursor.fetchall()
    r['num_declined_plans'] = num_declined_plans[0][0]

    # Get number of waiting for approval maintenance plans
    cursor.execute("""SELECT COUNT(plan_id) 
                    FROM maintenance_plan
                    WHERE status = 'waiting'""")
    num_waiting_plans = cursor.fetchall()
    r['num_waiting_plans'] = num_waiting_plans[0][0]

    # Get committe balance
    committe_balance = cursor.callfunc('COMMITTE_BALANCE', int)
    r['committe_balance'] = committe_balance

    return jsonify(r)
