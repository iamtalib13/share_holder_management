import frappe
import psycopg2
from psycopg2.extras import DictCursor

@frappe.whitelist()
def balance_inquiry(account_number=None):
    print("Starting Balance Inquiry...")  # Step 1: Execution started

    if not account_number:
        print("Error: Account number is required!")
        return

    conn_string = "host='10.60.133.66' dbname='finprd' user='postgres' password='ora123' port='2951'"
    print("Connection String Defined")  # Step 2: Connection string setup

    try:
        # Establish the connection
        print("Connecting to the database...")
        with psycopg2.connect(conn_string) as conn:
            print("Connected to the database")  # Step 3: Connected to DB

            # Use a cursor with DictCursor to fetch data as dictionaries
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                print(f"Executing query for account number: {account_number}")
                # Execute the SQL query with dynamic account number
                query = """
                    SELECT clr_bal_amt 
                    FROM tbaadm.gam 
                    WHERE foracid = %s;
                """
                cursor.execute(query, (account_number,))

                # Fetch one row
                result = cursor.fetchone()
                print("Query executed, fetching result...")  # Step 4: Query executed

                # Return only the balance if found
                if result:
                    print("Balance Fetched:", result['clr_bal_amt'])  # Step 5: Data fetched
                    return result['clr_bal_amt']
                else:
                    print("No balance found for this account.")
                    return 0  # Return 0 or null if no balance is found

    except psycopg2.Error as e:
        print(f"Database error: {e}")  # Step 6: Database error
    except Exception as e:
        print(f"Unexpected error: {e}")  # Step 7: General error
    finally:
        print("Execution Completed.")  # Step 8: Execution finished