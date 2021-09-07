""" 
The following is a Flask application that is set up with a Oracle SQL DB connection.

** Contributors **
Omer Lev-Ron
Sam Media
 
"""

from flask import Flask, request
from db_manager import init_db
from api.tenants import tenants_bp
from api.payments import payments_bp
from api.jobs import jobs_bp


app = Flask(__name__)

# Register Blueprints
app.register_blueprint(tenants_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(jobs_bp)


@app.route("/")
def index():
    return "<p>Index Page</p>"

#  Register a flask cli command to initalize the DB
@app.cli.command()
def initdb():
    """Clear the existing data and create new tables. Run with 'flask initdb' """
    init_db()
    print('Initialized the database.')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
