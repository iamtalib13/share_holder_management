import frappe
import frappe as _frappe

@frappe.whitelist()
def get_share_data():
    return frappe.db.sql(
        f"""select department,division,region,user_id,branch from `tabEmployee`;""",
        as_dict=True,
    )


import cx_Oracle
import frappe
from frappe.utils.pdf import get_pdf
from datetime import datetime
import cx_Oracle
import frappe
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def test_db(branch_code, ac_code, ac_no, start_date, end_date):
    connection = None  # Initialize connection variable
    cursor = None  # Initialize cursor variable
    try:
        print(f"Received inputs - Branch Code: {branch_code}, Account Code: {ac_code}, Account Number: {ac_no}, Start Date: {start_date}, End Date: {end_date}")

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        print(f"Parsed dates - Start Date: {start_date}, End Date: {end_date}")

        # Database connection parameters
        username = "sahyog"
        password = "sahyog"
        host = "10.0.115.20"
        port = "1521"
        sid = "orcl"
        print(f"Database connection parameters - Host: {host}, Port: {port}, SID: {sid}")

        # Create DSN and connect
        dsn = cx_Oracle.makedsn(host, port, service_name=sid)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        cursor = connection.cursor()
        print("Database connection established.")

        # 1. Fetch Branch Name and Code
        cursor.execute(
            "SELECT branchname, branchcode FROM SAHYOG.BRANCHMAS WHERE branchcode = :branch_code",
            {'branch_code': branch_code}
        )
        branch_result = cursor.fetchone()
        if not branch_result:
            frappe.throw("Branch not found for the given Branch Code.")
        branch_name, branch_code = branch_result
        print(f"Branch Name: {branch_name}, Branch Code: {branch_code}")

        # Mapping dictionary for ACMASTCODE to table names
        acmastcode_to_table = {
            157: 'CURMAS', 419: 'CURMAS', 444: 'CURMAS', 500: 'CURMAS', 628: 'CURMAS',
            255: 'CURMAS', 288: 'CURMAS', 442: 'CURMAS', 305: 'CURMAS', 324: 'CURMAS',
            564: 'CURMAS', 605: 'SAVMAS', 377: 'SAVMAS', 143: 'SAVMAS', 627: 'SAVMAS',
            445: 'SAVMAS', 559: 'SAVMAS', 3: 'SAVMAS', 385: 'SAVMAS', 431: 'SAVMAS',
            22: 'LNMAS', 25: 'LNMAS', 245: 'LNMAS', 152: 'LNMAS', 474: 'LNMAS',
            619: 'LNMAS', 386: 'LNMAS', 457: 'LNMAS', 620: 'LNMAS', 26: 'LNMAS',
            21: 'LNMAS', 20: 'LNMAS', 365: 'LNMAS', 223: 'LNMAS', 250: 'LNMAS',
            306: 'LNMAS', 24: 'LNMAS', 622: 'LNMAS', 23: 'LNMAS', 352: 'LNMAS',
            453: 'LNMAS', 482: 'LNMAS', 557: 'LNMAS', 615: 'LNMAS', 451: 'LNMAS',
            383: 'LNMAS', 623: 'LNMAS', 27: 'LNMAS', 18: 'LNMAS', 195: 'LNMAS',
            196: 'LNMAS', 421: 'LNMAS', 221: 'LNMAS', 405: 'LNMAS', 503: 'LNMAS',
            517: 'LNMAS', 621: 'LNMAS', 19: 'LNMAS', 159: 'LNMAS', 338: 'LNMAS',
            373: 'LNMAS', 343: 'LNMAS', 548: 'LNMAS', 617: 'LNMAS', 618: 'LNMAS',
            380: 'SSDMAS',
            418: 'SSDMAS', 328: 'SSDMAS', 142: 'SSDMAS', 216: 'SSDMAS', 1: 'FDMAS',
            247: 'FDMAS', 194: 'FDMAS', 155: 'FDMAS', 599: 'FDMAS', 2: 'FDMAS',
            148: 'FDMAS', 149: 'FDMAS', 4: 'FDMAS', 432: 'FDMAS', 233: 'FDMAS',
            154: 'FDMAS', 256: 'FDMAS', 290: 'SHMAS', 480: 'BA_MASTER', 561: 'INVMAS',
            609: 'INVMAS', 392: 'INVMAS', 519: 'INVMAS', 514: 'INVMAS', 568: 'INVMAS',
            287: 'INVMAS', 520: 'INVMAS', 160: 'INVMAS', 448: 'INVMAS', 501: 'INVMAS'
        }

        # Step 1: Fetch ACMASTCODE using AC_CODE
        cursor.execute(
            "SELECT ACMASTCODE,AC_NAME FROM SAHYOG.ACMAST WHERE AC_CODE = :ac_code",
            {'ac_code': ac_code}
        )
        acmastcode_result = cursor.fetchone()

        if not acmastcode_result:
            frappe.throw("ACMASTCODE not found for the given AC_CODE.")

        acmastcode, ac_name = acmastcode_result  # Get AC_NAME
        print(f"ACMASTCODE: {acmastcode}, AC_NAME: {ac_name}")

        # Step 2: Get the corresponding table name
        table_name = acmastcode_to_table.get(acmastcode)

        if not table_name:
            frappe.throw(f"Table mapping not found for ACMASTCODE: {acmastcode}")

        print(f"Table Name: {table_name}")

        # Step 3: Dynamically fetch GMST_CODE
        query = f"""
            SELECT GMST_CODE
            FROM SAHYOG.{table_name}
            WHERE AC_NO = :ac_no
            AND ACMASTCODE = :acmastcode
            AND BRANCHCODE = :branch_code
        """

        try:
            cursor.execute(query, {
                'ac_no': ac_no,
                'acmastcode': acmastcode,
                'branch_code': branch_code
            })
            gmst_code_result = cursor.fetchone()

            if not gmst_code_result:
                frappe.throw("GMST_CODE not found for the given criteria.")

            gmst_code = gmst_code_result[0]
            print(f"GMST_CODE: {gmst_code}")

        except Exception as e:
            frappe.throw(f"An error occurred while fetching GMST_CODE: {str(e)}")



        # 4. Fetch customer details using GMST_CODE
        cursor.execute(
            """
            SELECT name, addr, city, adharno, mobileno
            FROM SAHYOG.BANKMAS
            WHERE GMST_CODE = :gmst_code
            """,
            {'gmst_code': gmst_code}
        )
        customer_details = cursor.fetchone()
        if not customer_details:
            frappe.throw("Customer details not found for the provided GMST_CODE.")
        print(f"Customer Details: {customer_details}")

        customer_info = {
            "name": customer_details[0],
            "address": customer_details[1],
            "city": customer_details[2],
            "aadhar": customer_details[3],
            "telephone": customer_details[4],  # Use mobileno for 'telephone'
        }

        # 5. Calculate opening balance
        print("Calculating opening balance...")
        cursor.execute(
            """
            SELECT 
                NVL(SUM(CASE WHEN credit > 0 THEN credit ELSE 0 END), 0) - 
                NVL(SUM(CASE WHEN debit > 0 THEN debit ELSE 0 END), 0) AS opening_balance
            FROM 
                SAHYOG.ACBK
            WHERE 
                AC_NO = :ac_no 
                AND FORBRANCH = :branch_code 
                AND ACMASTCODE = :acmastcode 
                AND tdate < :start_date
                AND POST = 1
                AND (cncled != 1 OR cncled IS NULL)
                ORDER BY ctrnno  -- Order by ctrnno for proper sequence
            """,
            {
                'ac_no': ac_no,
                'branch_code': branch_code,
                'acmastcode': acmastcode,
                'start_date': start_date
            }
        )
        opening_balance = cursor.fetchone()[0] or 0  # Get opening balance
        print(f"Opening Balance: {opening_balance}")

        # 6. Fetch previous records before the start date
        print("Fetching previous records...")
        cursor.execute(
            """
            SELECT tdate, credit, debit, prtcls
            FROM SAHYOG.ACBK
            WHERE AC_NO = :ac_no 
              AND FORBRANCH = :branch_code 
              AND ACMASTCODE = :acmastcode 
              AND tdate < :start_date
              AND POST = 1
              AND (cncled != 1 OR cncled IS NULL)
            ORDER BY ctrnno  -- Order by ctrnno for proper sequence
            """,
            {
                'ac_no': ac_no,
                'branch_code': branch_code,
                'acmastcode': acmastcode,
                'start_date': start_date
            }
        )
        previous_records = cursor.fetchall()
        print(f"Prev records: {previous_records}")

        # 7. Fetch transactions within the specified date range
        print("Fetching transactions between start and end dates...")
        cursor.execute(
            """
            SELECT tdate, credit, debit, prtcls, doc_no
            FROM SAHYOG.ACBK
            WHERE AC_NO = :ac_no 
              AND FORBRANCH = :branch_code 
              AND ACMASTCODE = :acmastcode 
              AND tdate BETWEEN :start_date AND :end_date
              AND POST = 1
              AND (cncled != 1 OR cncled IS NULL)
            ORDER BY ctrnno  -- Order by ctrnno for proper sequence
            """,
            {
                'ac_no': ac_no,
                'branch_code': branch_code,
                'acmastcode': acmastcode,
                'start_date': start_date,
                'end_date': end_date
            }
        )
        transactions = cursor.fetchall()
        print(f"Transactions: {transactions}")

        # 8. Prepare transaction data for rendering
       # Prepare transaction data for rendering
        transaction_data = []
        current_balance = opening_balance

        # Format opening balance to two decimal places
        opening_balance = round(opening_balance, 2)

        # # Process previous records
        # for record in previous_records:
        #     tdate, credit, debit, prtcls = record
        #     credit = float(credit) if credit else 0.0
        #     debit = float(debit) if debit else 0.0
        #     current_balance += (credit - debit)  # Update the current balance for previous records
            
        #     # Format the values to two decimal places
        #     transaction_data.append({
        #         'transaction_date': tdate,
        #         'transaction_type': 'Debit' if debit > 0 else 'Credit',
        #         'description': prtcls,
        
        #         'doc_no': '',  # Add document number if available
        #         'debit': debit,  # Format to 2 decimal places
        #         'credit': credit,  # Format to 2 decimal places
        #         'balance': round(current_balance, 2)  # Format to 2 decimal places
        #     })

                # Process current transactions
        for record in transactions:
            tdate, credit, debit, prtcls, doc_no = record
            credit = float(credit) if credit else 0.0
            debit = float(debit) if debit else 0.0
            current_balance += (credit - debit)  # Update the current balance for current transactions
            
            # Format the values to two decimal places
            transaction_data.append({
                'transaction_date': tdate.strftime("%d/%m/%Y"),
                'transaction_type': 'Debit' if debit > 0 else 'Credit',
                'description': prtcls,
                'doc_no': doc_no,
                'debit': round(debit, 2),  # Format to 2 decimal places
                'credit': round(credit, 2),  # Format to 2 decimal places
                'balance': round(current_balance, 2)  # Format to 2 decimal places
            })


        # Prepare context for rendering the PDF
        context = {
            "customer_info": customer_info,  # Include customer_info in the context
            "transactions": transaction_data,
            "branch_code": branch_code,
            "branch_name":branch_name,
            "ac_no": ac_no,
            "ac_name": ac_name,  # Include AC_NAME
            "start_date": start_date.strftime("%d/%m/%Y"),
            "end_date": end_date.strftime("%d/%m/%Y"),
            "opening_balance": opening_balance,
        }

        # Render PDF using a template
        html_content = frappe.render_template("templates/transaction_statement.html", context)
        pdf_data = get_pdf(html_content)

        # Return PDF as response
        frappe.local.response.filename = f"Transaction_Statement_{ac_no}.pdf"
        frappe.local.response.filecontent = pdf_data
        frappe.local.response.type = "download"

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        frappe.throw(f"Database error: {error.message}")
    except Exception as e:
        frappe.throw(str(e))
    finally:
        if cursor:
            cursor.close()  # Ensure the cursor is closed
        if connection:
            connection.close()  # Ensure the connection is closed
