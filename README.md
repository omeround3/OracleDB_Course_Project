# Oracle DB - Course Project
The project implements an Oracle XE Database for a joint house commite system.

- The system supports tenant payments, maintenance work, and committee elections.
- The system will allow inserting the details of the tenants of the apartments in the building (such as last name, number of tenants in the apartment, size of the apartment, etc.) as well as updating the details of the tenants. The payment rate and its date are determined according to the details of the tenants and the apartment.
- The tenants of the building make monthly payments. The system allows to insert the payment details (apartment number, tenant name, date, amount and purpose of payment), and generate a receipt for the payer.
- The system allows, at the request of the committee member, the production of payment reports and debts for different periods, for all tenants or some of them. The system will also present on demand the balance of funds in the committee's possession.
- Any tenant can apply to carry out work on the common property. Committee members prepare maintenance plans for implementation and feed them into the system. Each plan is fed according to the type (landscaping, painting, etc.).

# ERD Diagram
![picture alt](https://github.com/omeround3/OracleDB_Course_Project/blob/main/DB_Model/Committe_v3.png)


# Tools Used
- Oracle SQL Data Modeler
- Oracle SQL Developer
- Docker (running Oracle XE 18c image)
- Python
- Flask - The project's backend web framework
- Angluar - The project's frontend web framework
- Digital Ocean - Cloud Computing Platform

**Architecture Diagram**
![picture alt](https://github.com/omeround3/OracleDB_Course_Project/blob/main/Oracle%20DB%20Project%20Diagram.jpeg)

# How to run
1. Clone this repository to the the machine you would like to run it from (`clone https://github.com/omeround3/OracleDB_Course_Project.git`)
2. Install python virtual enviroment using `python3 -m pip install --user virtualenv` on macOS or Linux. On Windows run `py -m pip install --user virtualenv`
3. Create a virtual enviroment using `python3 -m venv env` on macOS or Linux. On Windows run `py -m venv env`
4. Activate the virutal enviroment using `source env/bin/activate` on macOS or Linux. On Windows run `.\env\Scripts\activate`
5. Go into the project directory `cd OracleDB_Course_Project`
6. Install dependendcies using `pip install -r requirements.txt`(this might takes a couple of minutes, don't close the terminal).
7. Run the server using `flask run` (default port is 5000). Read more about Flask framework understand all the running and deployment options.

# Database setup and configurations
You can set up the database with any method mentioned in the documentation. References:
- https://docs.oracle.com/cd/E17781_01/install.112/e18803/toc.htm#XEINW102
- https://blogs.oracle.com/oraclemagazine/deliver-oracle-database-18c-express-edition-in-containers
- https://hub.docker.com/r/vitorfec/oracle-xe-18c

## The Docker Image we used in the project
We used the following Oracle Database XE Docker image
- https://hub.docker.com/r/vitorfec/oracle-xe-18c

Basically, if you installed Docker in your enviorment. The only command you need is:
`docker run --name OracleXE --shm-size=1g -p 1521:1521 -p 8080:8080 -e ORACLE_PWD=password vitorfec/oracle-xe-18c`

#### Parameters Explanation
- `--name OracleXE` - Docker container name
- `-p 1521:1521` - Database connection port mapping
- `-e ORACLE_PWD=password` - change `password` for the password you want to connect with to the database.


## Backend database connection configurations
In the Flask backend, you need to edit the `config.py` file and configure the database connection settings.
