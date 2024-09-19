import frappe
from frappe.utils import now
from frappe.utils.data import now_datetime
<<<<<<< HEAD
=======
import frappe
import psycopg2 # type: ignore
import psycopg2.extras # type: ignore
import frappe
from psycopg2.extras import DictCursor # type: ignore

from datetime import datetime

from datetime import datetime
import frappe

def convert_date_format(date_str, input_format='%d-%m-%Y', output_format='%Y-%m-%d'):
    """Convert date string from input_format to output_format."""
    try:
        if date_str:
            return datetime.strptime(date_str, input_format).strftime(output_format)
    except ValueError:
        # Handle the case where the date format is incorrect
        return None
    return None

def create_or_update_share_application(data):
    try:
        # Convert date fields to the correct format
        cif_creation_dt = convert_date_format(data.get('cif_creation_dt'))
        account_opening_date = convert_date_format(data.get('account_opening_date'))
        date_of_birth = convert_date_format(data.get('birth_date'))

        # Check if a Share Application already exists for the given customer_id
        existing_application = frappe.db.get_value("Share Application", {"customer_id": data.get('customer_id')})

        if existing_application:
            # Update existing Share Application
            share_app = frappe.get_doc("Share Application", existing_application)
            share_app.update({
                "salutation": data.get('salutation', None),
                "customer_name": data.get('customer_name', None),
                "date_of_birth": date_of_birth,
                "gender": data.get('gender', None),
                "address": data.get('address_line1', None),
                "city": data.get('city', None),
                "state": data.get('state', None),
                "pin_code": data.get('zip', None),
                "mobile": data.get('mobile', None),
                "occupation": data.get('occupation', None),
                "aadhaar_number": data.get('aadhaar_number', None),
                "branch": data.get('branch', None),
                "branch_code": data.get('branch_code', None),
                "ac_open_dt": cif_creation_dt,
                "application_date": cif_creation_dt,
                "saving_current_ac_no": data.get('acct_num', None),
                "fin_account_type": data.get('account_type', None),
                "gl_sub_head_code": data.get('gl_sub_head_code', None),
                "account_opening_date": account_opening_date,
                "status": "Submitted"
            })
            share_app.save()
            frappe.db.commit()
            print(f"Updated Share Application for customer_id: {data.get('customer_id')}")
        else:
            # Create a new Share Application
            share_app = frappe.get_doc({
                "doctype": "Share Application",
                "customer_id": data.get('customer_id'),
                "salutation": data.get('salutation', None),
                "customer_name": data.get('customer_name', None),
                "date_of_birth": date_of_birth,
                "gender": data.get('gender', None),
                "address": data.get('address_line1', None),
                "city": data.get('city', None),
                "state": data.get('state', None),
                "pin_code": data.get('zip', None),
                "mobile": data.get('mobile', None),
                "occupation": data.get('occupation', None),
                "aadhaar_number": data.get('aadhaar_number', None),
                "branch": data.get('branch', None),
                "branch_code": data.get('branch_code', None),
                "ac_open_dt": cif_creation_dt,
                "application_date": cif_creation_dt,
                "saving_current_ac_no": data.get('acct_num', None),
                "fin_account_type": data.get('account_type', None),
                "gl_sub_head_code": data.get('gl_sub_head_code', None),
                "account_opening_date": account_opening_date,
                "status": "Submitted"
            })
            share_app.insert()
            frappe.db.commit()
            print(f"Created Share Application for customer_id: {data.get('customer_id')}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error processing Share Application for customer_id: {data.get('customer_id')}")
        print(f"Error processing Share Application for customer_id: {data.get('customer_id')} - {str(e)}")

def check_db_and_sync():
    conn_string = "host='10.60.133.66' dbname='finprd' user='custom' password='custom' port='2951'"
    
    conn = None
    cursor = None
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=DictCursor)

        if conn:
            print("Connected to the database")
            cursor.execute("SELECT * FROM custom.c_shares")
            rows = cursor.fetchall()

            for row in rows:
                data = dict(row)  # Convert row to dictionary
                create_or_update_share_application(data)  # Create or update Share Application
        else:
            print("Failed to connect to the database")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in database synchronization")
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed")

def ping():
    print("pong")
        
>>>>>>> 61341525119f66acfe8a57c6aa49655a69426c63

def cron():
    tickets = frappe.get_all(
        "Share Application",
        filters={"status": "update"},
        fields=["name", "ac_no", "share_ac_no", "status"],
        order_by="modified DESC",
    )

    for ticket in tickets:
        account_number = ticket.ac_no
        application_sr_no = ticket.name

        # Transfer the value of "ac_no" to "share_ac_no"
        frappe.db.set_value(
            "Share Application",
            application_sr_no,
            "share_ac_no",
            account_number,
            update_modified=False,
        )

        # Set "ac_no" to null
        frappe.db.set_value(
            "Share Application", application_sr_no, "ac_no", None, update_modified=False
        )

    frappe.db.commit()  # Commit changes after updating all records

    print("\n\nUpdated share accounts where status is 'update'\n\n")


def test():
    tickets = frappe.get_all(
        "Share Test",
        filters={"status": "Sanctioned"},
        fields=["name", "share_application_no", "no_of_shares", "status"],
    )

    last_end_range = 0

    for ticket in sorted(tickets, key=lambda x: x.name):
        application_sr_no = ticket.share_application_no
        id = ticket.name
        no_of_shares = ticket.no_of_shares

        # Calculate start_range and end_range based on no_of_shares
        start_range = last_end_range + 1
        end_range = start_range + no_of_shares - 1

        # Update start_range and end_range in the Share Test record
        frappe.db.set_value(
            "Share Test", id, "start_range", start_range, update_modified=False
        )
        frappe.db.set_value(
            "Share Test", id, "end_range", end_range, update_modified=False
        )

        # Update last_end_range for the next iteration
        last_end_range = end_range

    frappe.db.commit()  # Commit changes after updating all records

    print("\n\nUpdated range '\n\n")


def update():
    batch_size = 30000  # Adjust the batch size as needed
    total_records = 362963
    processed_records = 0

    while processed_records < total_records:
        tickets = frappe.get_all(
            "Share Application",
            filters={"status": "Sanctioned"},
            fields=["name", "status"],
            start=processed_records,
            limit=batch_size,
        )

        if not tickets:
            break  # No more records

        for ticket in tickets:
            id = ticket.name

            try:
                # Update status to "Sanctioned"
                frappe.db.set_value(
                    "Share Application",
                    id,
                    "status",
                    "Sanctioned",
                    update_modified=False,
                )
                print(f"Updated record {id}")
            except Exception as e:
                print(f"Error updating record {id}: {e}")

        frappe.db.commit()  # Commit changes after updating each batch
        processed_records += batch_size

    print("\n\nUpdated status to 'Sanctioned' for records with status 'Draft'\n\n")


def branches():
    # Query to get distinct branches
    query = """
        SELECT DISTINCT branch
        FROM `tabUser`
        WHERE role_profile_name = 'Share User Employee';
    """

    # Fetch distinct branches from the database
    result_branches = frappe.db.sql(query, as_dict=True)

    if result_branches:
        print("\nDistinct Branches:")

        # Loop through each branch and print
        for index, branch in enumerate(result_branches, start=1):
            print(f"{index}. {branch.get('branch')}")

    else:
        print("\nNo branches found.")


# to all end branches day
@frappe.whitelist()
def day_end(datetime_str, userId, employeeName):
    """
    Start the day for all branches with the given datetime, employee ID, and employee name.
    """
    try:
        # Parse the provided datetime string into a datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

        # Fetch distinct branches from the database
        result_branches = frappe.db.sql(
            """
            SELECT DISTINCT branch
            FROM `tabUser`
            WHERE role_profile_name = 'Share User Employee'
            """,
            as_dict=True,
        )

        if result_branches:
            frappe.log("Creating Day End Documents:")

            # Loop through each branch and create a Day Management Checkin document
            for branch in result_branches:
                # Create a new document
                doc = frappe.new_doc("Day Management Checkin")
                doc.branch = branch.get("branch")
                doc.log_type = "End"
                doc.log_time = datetime_obj  # Use the provided datetime
                doc.employee = userId
                doc.emp_name = employeeName

                try:
                    doc.insert()
                    frappe.log(
                        f"Created Day End Document for Branch {branch.get('branch')} with employee {employeeName}"
                    )
                except frappe.DuplicateEntryError:
                    frappe.log(
                        f"Day End for Branch {branch.get('branch')} with employee {employeeName} already exists.",
                        level="warn",
                    )

        else:
            frappe.log("No branches found for day End")

    except Exception as e:
        frappe.log_error(f"Error in day_end: {e}", title="Day end Error")
        frappe.throw(str(e))


from frappe.utils import now_datetime

from datetime import datetime


@frappe.whitelist()
def day_start(datetime_str, userId, employeeName):
    """
    Start the day for all branches with the given datetime, employee ID, and employee name.
    """
    try:
        # Parse the provided datetime string into a datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

        # Fetch distinct branches from the database
        result_branches = frappe.db.sql(
            """
            SELECT DISTINCT branch
            FROM `tabUser`
            WHERE role_profile_name = 'Share User Employee'
            """,
            as_dict=True,
        )

        if result_branches:
            frappe.log("Creating Day Start Documents:")

            # Loop through each branch and create a Day Management Checkin document
            for branch in result_branches:
                # Create a new document
                doc = frappe.new_doc("Day Management Checkin")
                doc.branch = branch.get("branch")
                doc.log_type = "Start"
                doc.log_time = datetime_obj  # Use the provided datetime
                doc.employee = userId
                doc.emp_name = employeeName

                try:
                    doc.insert()
                    frappe.log(
                        f"Created Day Start Document for Branch {branch.get('branch')} with employee {employeeName}"
                    )
                except frappe.DuplicateEntryError:
                    frappe.log(
                        f"Day Start for Branch {branch.get('branch')} with employee {employeeName} already exists.",
                        level="warn",
                    )

        else:
            frappe.log("No branches found for day start")

    except Exception as e:
        frappe.log_error(f"Error in day_start: {e}", title="Day Start Error")
        frappe.throw(str(e))


def update_barcode():
    print("barcode updated")


def update_base():
    batch_size = 30000  # Adjust the batch size as needed
    total_records = 362963
    processed_records = 0

    while processed_records < total_records:
        tickets = frappe.get_all(
            "Share Application",
            filters={"status": "Sanctioned"},
            fields=["name", "status", "no_of_shares", "base_share_amount"],
            start=processed_records,
            limit=batch_size,
        )

        if not tickets:
            break  # No more records

        for ticket in tickets:
            id = ticket.name

            try:
                # Set base_share_amount to the calculated value
                frappe.db.set_value(
                    "Share Application",
                    id,
                    "share_application_charges",
                    10,
                    update_modified=False,
                )
                print(f"Set share appliction charges to 10 for record {id}")

            except Exception as e:
                print(f"Error updating record {id}: {e}")

        frappe.db.commit()  # Commit changes after updating each batch
        processed_records += batch_size

    print("\n\nUpdated base_share_amount based on no_of_shares\n\n")


def update_share_account():
    batch_size = 30000  # Adjust the batch size as needed
    total_records = 362959
    processed_records = 0
    share_ac_no = 1  # Initialize share_ac_no
    customer_share_mapping = {}  # Dictionary to map customer_id to share_ac_no
    current_id = 1  # Start from id 1

    while current_id <= total_records:
        # Processing records in batches
        for _ in range(batch_size):
            if current_id > total_records:
                break  # Stop processing if current_id exceeds total_records

            ticket = frappe.get_doc("Share Application", current_id)

            if not ticket:
                print("No more records to update.")
                break  # No more records

            id = ticket.name
            customer_id = ticket.customer_id

            try:
                # Clear share_ac_no first
                frappe.db.set_value(
                    "Share Application", id, "share_ac_no", None, update_modified=False
                )

                # Assign share_ac_no based on customer_id
                if customer_id in customer_share_mapping:
                    share_ac_no = customer_share_mapping[customer_id]
                else:
                    # Retrieve the correct share_ac_no for existing customer_id
                    share_ac_no = frappe.get_value(
                        "Share Application", {"customer_id": customer_id}, "share_ac_no"
                    )

                    if not share_ac_no:
                        # If share_ac_no doesn't exist, generate a new one
                        share_ac_no = (
                            max(customer_share_mapping.values(), default=0) + 1
                        )
                        customer_share_mapping[customer_id] = share_ac_no

                # Set share_ac_no in the Share Application record
                frappe.db.set_value(
                    "Share Application",
                    id,
                    "share_ac_no",
                    share_ac_no,
                    update_modified=False,
                )
                print(
                    f"Assigned share_ac_no {share_ac_no} to record {id} for customer {customer_id}"
                )

            except Exception as e:
                print(f"Error updating record {id}: {e}")

            processed_records += 1  # Move to the next record
            current_id += 1

        frappe.db.commit()  # Commit changes after processing each batch

    print("\n\nUpdated share_ac_no based on customer_id\n\n")


def check_first_10_records_serially():
    batch_size = 1  # Process one record at a time
    total_records_to_check = 10
    processed_records = 0
    current_id = 1  # Start from id 1

    while processed_records < total_records_to_check:
        ticket = frappe.get_doc("Share Application", current_id)

        if not ticket:
            print("No more records to check.")
            break  # No more records

        print(f"Checking record {ticket.name} for customer {ticket.customer_id}")

        processed_records += 1  # Move to the next record
        current_id += 1

    print("\n\nChecked first 10 records serially\n\n")


import frappe

import frappe

import frappe

import frappe
import json
import xml.etree.ElementTree as ET


@frappe.whitelist(allow_guest=True)
def get_employees():
    # JSON data
    json_data = {
        "city": "San Jose",
        "firstName": "John",
        "lastName": "Doe",
        "state": "CA",
    }

    # Convert JSON to XML
    xml_data = convert_json_to_xml(json_data)

    frappe.response["content_type"] = "application/xml"
    frappe.response["message"] = xml_data


def convert_json_to_xml(json_data):
    root = ET.Element("root")
    for key, value in json_data.items():
        sub_element = ET.SubElement(root, key)
        sub_element.text = str(value)
    return ET.tostring(root, encoding="unicode")



def test_db():
    # Database connection details
    conn_string = "host='10.60.133.66' dbname='finprd' user='custom' password='custom' port='2951'"
    
    conn = None
    cursor = None
    
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Check if the connection is successful
        if conn:
            print("Connected to the database")
            
            # Execute a SQL query to fetch all records from the custom.c_shares table
            cursor.execute("SELECT * FROM custom.c_shares")
            
            # Fetch all rows from the executed query
            rows = cursor.fetchall()
            
            # Print each row
            for row in rows:
                print(dict(row))  # Convert each row to a dictionary for better readability

        else:
            print("Failed to connect to the database")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed")