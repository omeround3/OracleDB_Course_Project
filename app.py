from flask import Flask, jsonify,request
from db_manager import connect


app = Flask(__name__)

cursor= None

@app.route("/")
def index():
    cursor = connect()
    return "<p>Index Page</p>"

@app.route("/tenants/")
def tenants():
    name = request.args.get('name')
    if name:
        cursor.execute(f"SELECT * FROM tenant WHERE FIRST_NAME LIKE '{name}%' or LAST_NAME like '{name}%'")
        r = cursor.fetchall()
        return jsonify(r)
    cursor.execute("select * from tenant")
    r = cursor.fetchall()
    return jsonify(r)

@app.route("/jobs/")
def jobs():
    id = request.args.get('id')
    if id:
        cursor.execute(f"SELECT * FROM JOBS WHERE TENANT_ID={id}")
        r = cursor.fetchall()
        return jsonify(r)
    cursor.execute("select * from JOBS")
    r = cursor.fetchall()
    print(r)
    return jsonify(r)

if __name__ == "__main__":
    cursor = connect()
    app.run(host='0.0.0.0')
