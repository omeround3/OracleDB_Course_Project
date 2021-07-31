# Oracle DB - Course Project
The project implements an Oracle XE Database for a joint house commite system.

- The system supports tenant payments, maintenance work, and committee elections.
- The system will allow inserting the details of the tenants of the apartments in the building (such as last name, number of tenants in the apartment, size of the apartment, etc.) as well as updating the details of the tenants. The payment rate and its date are determined according to the details of the tenants and the apartment.
- The tenants of the building make payments by check or cash. The system allows committee members to insert the payment details (apartment number, tenant name, date, amount and purpose of payment), and generate a receipt for the payer.
- The system allows, at the request of the committee member, the production of payment reports and debts for different periods, for all tenants or some of them. The system will also present on demand the balance of funds in the committee's possession.
- Any tenant can apply to carry out work on the common property. Committee members prepare maintenance plans for implementation and feed them into the system. Each plan is fed according to the type (landscaping, painting, etc.).

## Tools Used
- Oracle SQL Data Modeler
- Oracle SQL Developer
- Docker (running Oracle XE 18c image)
- Python


## How to run
