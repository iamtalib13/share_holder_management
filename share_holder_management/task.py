import frappe


def update_share_ac():

    # Fetch the first 10 Sahayog Ticket records with name from 1 to 10
    tickets = frappe.get_all(
        "Share Application",
        filters={"name": ["between", 1, 10]},
        fields=[
            "name",
            "ac_no",
            "share_ac_no",
        ],
    )

    for ticket in tickets:
        account_number = ticket.ac_no
        application_sr_no = ticket.name

        # Transfer the value of "ac_no" to "share_ac_no"
        frappe.db.set_value("Share Application", application_sr_no, "share_ac_no", account_number, update_modified=False)
        
        # Set "ac_no" to null
        frappe.db.set_value("Share Application", application_sr_no, "ac_no", None, update_modified=False)

    frappe.db.commit()
    print("\n\nUpdated share accounts\n\n")
    
    
    
    
############################### Sahayog Statement #################################################
# import frappe
# from frappe.utils.pdf import get_pdf
# from datetime import datetime

# # Pre-defined transactions dictionary
# transactions_data = [
#     {
#         "account_number": "1234567890",
#         "transaction_date": "2024-01-01",
#         "amount": 1000,
#         "transaction_type": "Credit",
#         "description": "Salary"
#     },
#     {
#         "account_number": "1234567890",
#         "transaction_date": "2024-01-05",
#         "amount": -200,
#         "transaction_type": "Debit",
#         "description": "Shopping"
#     },
#     {
#         "account_number": "9876543210",
#         "transaction_date": "2024-01-10",
#         "amount": 1500,
#         "transaction_type": "Credit",
#         "description": "Freelance"
#     },
#     {
#         "account_number": "1234567890",
#         "transaction_date": "2024-01-15",
#         "amount": -500,
#         "transaction_type": "Debit",
#         "description": "Electricity Bill"
#     },
# ]

# @frappe.whitelist(allow_guest=True)
# def fetch_transactions(account_number, start_date, end_date):
#     # Convert string dates to datetime
#     start_date = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
#     # Filter transactions based on input
#     filtered_transactions = [
#         t for t in transactions_data
#         if t["account_number"] == account_number
#         and start_date <= datetime.strptime(t["transaction_date"], "%Y-%m-%d") <= end_date
#     ]
    
#     if not filtered_transactions:
#         frappe.throw("No transactions found for the given criteria.")
    
#     # Render HTML for PDF
#     html_content = frappe.render_template("templates/transaction_statement.html", {
#         "transactions": filtered_transactions
#     })
#     pdf_data = get_pdf(html_content)
    
#     # Return PDF as response
#     frappe.local.response.filename = "Transaction_Statement.pdf"
#     frappe.local.response.filecontent = pdf_data
#     frappe.local.response.type = "download"
    
@frappe.whitelist(allow_guest=True)    
def ping():
    return "xyz"



###################################################################
# Database Connection Details for Statement Generation
###################################################################
import cx_Oracle


# Connection Parameters (already initialized)
username = "system"
password = "sahyog"
host = "localhost"
port = "1521"  # Default port for Oracle
sid = "orcl"   # SID or service name

def connect_to_oracle():
    """
    Connect to an Oracle database using pre-initialized parameters and perform operations.
    """
    # Create a DSN (Data Source Name)
    dsn = cx_Oracle.makedsn(host, port, service_name=sid)

    try:
        # Establish the connection
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        print("Connection successful!")

        # Perform database operations here
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM v$version")
        result = cursor.fetchall()
        print("Oracle Version Info:")
        for row in result:
            print(row)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"An error occurred: {error.message}")
    
    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection:
            connection.close()
            print("Connection closed.")
