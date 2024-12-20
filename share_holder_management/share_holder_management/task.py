import argparse
import frappe
from frappe.utils import now
from frappe.utils.data import now_datetime
import frappe
import psycopg2 # type: ignore
import psycopg2.extras # type: ignore
import frappe
from psycopg2.extras import DictCursor # type: ignore


from datetime import datetime

from datetime import datetime
import frappe


@frappe.whitelist(allow_guest=True)
def test_print():
    return "Work kar raha hai"

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

        # Ensure that acct_num exists before proceeding
        acct_num = data.get('acct_num', None)
        if not acct_num:
            print(f"Account number missing for customer_id: {data.get('customer_id')}. Skipping creation.")
            return  # Exit the function if acct_num is missing

        # Check if a Share Application already exists for the given customer_id
        existing_application = frappe.db.get_value("Share Application", {"customer_id": data.get('customer_id')})

        if existing_application:
            # Update existing Share Application using db_set
            share_app = frappe.get_doc("Share Application", existing_application)
            
            fields_to_update = {
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
                "fin_account_type": data.get('account_type', None),
               
                
            }
            
            # Update fields using db_set with update_modified=False
            for field, value in fields_to_update.items():
                if value is not None:  # Only update non-None values
                    share_app.db_set(field, value, update_modified=False)

            frappe.db.commit()
            print(f"Updated Share Application for customer_id: {data.get('customer_id')}")
        else:
            # Create a new Share Application only if acct_num exists
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
                "saving_current_ac_no": acct_num,
                "fin_account_type": data.get('account_type', None),
                "gl_sub_head_code": data.get('gl_sub_head_code', None),
                "account_opening_date": account_opening_date,
                "status": "Submitted"
            })
            share_app.insert(ignore_permissions=True)
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

# def ping():
#     print("pong")
    
def check_db():
    conn_string = "host='10.60.133.66' dbname='finprd' user='custom' password='custom' port='2951'"
    
    try:
        with psycopg2.connect(conn_string) as conn:
            print("Connected to the database")
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT customer_id,acct_num,customer_name,cif_creation_dt FROM custom.c_shares;")
                for row in cursor.fetchall():
                    print(dict(row))  # Print the data as a dictionary
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Database connection closed") 



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


import frappe
import random
import requests
import xmltodict
from datetime import datetime

def finacle_fund_transfer_api():
    # Fetch all Journal Entries with docstatus 0 that haven't been processed yet
    journal_entries = frappe.get_all('Journal Entry', filters={'docstatus': 0}, fields=['name'])

    for entry in journal_entries:
        entry_name = entry.name  # Get the name of each Journal Entry
        
        try:
            # Fetch the specific Journal Entry record
            entry_doc = frappe.get_doc('Journal Entry', entry_name, ignore_permissions=True)

            # Debit Customer Account Number
            debitor_account = None
            for child in entry_doc.accounts:
                if child.debit_in_account_currency > 0:
                    # Fetch the linked Account document
                    account_doc = frappe.get_doc('Account', child.account)
                    debitor_account = account_doc.account_number
                    break  # Exit the loop after finding the first matching record

            print("Debitor Account Number:", debitor_account)
             # Get the current date and time in the required format
            current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]  # Format to YYYY-MM-DDTHH:MM:SS.sss
            # Generate a random GUID (10-digit random number)
            guid = random.randint(1000000000, 9999999999)

            # XML Data to be sent
            xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<FIXML xsi:schemaLocation="http://www.finacle.com/fixml XferTrnAdd.xsd" xmlns="http://www.finacle.com/fixml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Header>
        <RequestHeader>
            <MessageKey>
                <RequestUUID>{guid}</RequestUUID>
                <ServiceRequestId>XferTrnAdd</ServiceRequestId>
                <ServiceRequestVersion>10.2</ServiceRequestVersion>
                <ChannelId>COR</ChannelId>
                <LanguageId></LanguageId>
            </MessageKey>
            <RequestMessageInfo>
                <BankId>01</BankId>
                <TimeZone></TimeZone>
                <EntityId></EntityId>
                <EntityType></EntityType>
                <ArmCorrelationId></ArmCorrelationId>
                <MessageDateTime>2024-12-11T00:00:00.000</MessageDateTime>
            </RequestMessageInfo>
            <Security>
                <Token>
                    <PasswordToken>
                        <UserId></UserId>
                        <Password></Password>
                    </PasswordToken>
                </Token>
                <FICertToken></FICertToken>
                <RealUserLoginSessionId></RealUserLoginSessionId>
                <RealUser></RealUser>
                <RealUserPwd></RealUserPwd>
                <SSOTransferToken></SSOTransferToken>
            </Security>
        </RequestHeader>
    </Header>
    <Body>
        <XferTrnAddRequest>
            <XferTrnAddRq>
                <XferTrnHdr>
                    <TrnType>T</TrnType>
                    <TrnSubType>CI</TrnSubType>
                </XferTrnHdr>
                <XferTrnDetail>
                    <!-- Debit Transaction -->
                    <PartTrnRec>
                        <AcctId>
                            <AcctId>{debitor_account}</AcctId>
                        </AcctId>
                        <CreditDebitFlg>D</CreditDebitFlg>
                        <TrnAmt>
                            <amountValue>20</amountValue>
                            <currencyCode>INR</currencyCode>
                        </TrnAmt>
                        <TrnParticulars>Share Fund Debited</TrnParticulars>
                        <PartTrnRmks>Share Fund Debited</PartTrnRmks>
                        <ValueDt>{current_date}</ValueDt>
                        <UserPartTrnCode></UserPartTrnCode>
                    </PartTrnRec>
                    <!-- Credit Transaction 1 -->
                    <PartTrnRec>
                        <AcctId>
                            <AcctId>100001410010001</AcctId>
                        </AcctId>
                        <CreditDebitFlg>C</CreditDebitFlg>
                        <TrnAmt>
                            <amountValue>10</amountValue>
                            <currencyCode>INR</currencyCode>
                        </TrnAmt>
                        <TrnParticulars>SHARE ACCOUNT</TrnParticulars>
                        <PartTrnRmks>SHARE ACCOUNT</PartTrnRmks>
                        <ValueDt>{current_date}</ValueDt>
                        <UserPartTrnCode></UserPartTrnCode>
                    </PartTrnRec>
                    <!-- Credit Transaction 2 -->
                    <PartTrnRec>
                        <AcctId>
                            <AcctId>100001670060001</AcctId>
                        </AcctId>
                        <CreditDebitFlg>C</CreditDebitFlg>
                        <TrnAmt>
                            <amountValue>10</amountValue>
                            <currencyCode>INR</currencyCode>
                        </TrnAmt>
                        <TrnParticulars>SHARE MEMBER ENTRY FEE</TrnParticulars>
                        <PartTrnRmks>SHARE MEMBER ENTRY FEE</PartTrnRmks>
                        <ValueDt>{current_date}</ValueDt>
                        <UserPartTrnCode></UserPartTrnCode>
                    </PartTrnRec>
                </XferTrnDetail>
            </XferTrnAddRq>
        </XferTrnAddRequest>
    </Body>
</FIXML>
"""

            # Set up the API request
            url = 'https://smcprd.sahayog.net.in:2950/FISERVLET/fihttp'
            headers = {'Content-Type': 'application/xml'}

            # Disable SSL verification and send the request
            response = requests.post(url, data=xml_data, headers=headers, verify=False)

            print(f"HTTP Status Code for {entry_name}: {response.status_code}")
            print("XML Response Received:\n" + response.text)

            if response.status_code == 200:
                try:
                    # Parse the XML response
                    response_dict = xmltodict.parse(response.text)

                    # Extracting specific fields from the XML
                    status = response_dict.get('FIXML', {}).get('Header', {}).get('ResponseHeader', {}).get('HostTransaction', {}).get('Status', '').strip()
                    custom_trn_id = response_dict.get('FIXML', {}).get('Body', {}).get('XferTrnAddResponse', {}).get('XferTrnAddRs', {}).get('TrnIdentifier', {}).get('TrnId', '').strip()

                    print(f"Transaction ID for {entry_name}: {custom_trn_id}, Status: {status}")

                    # Update the Journal Entry if the transaction is successful
                    if status == "SUCCESS":
                        entry_doc.db_set('docstatus', 1)
                        entry_doc.db_set('custom_api_response', response.text)
                        entry_doc.db_set('custom_finacle_transaction_id', custom_trn_id)
                        entry_doc.db_set('custom_status', status)
                    
                    else:
                        entry_doc.db_set('docstatus', 0)
                        entry_doc.db_set('custom_api_response', response.text)
                        entry_doc.db_set('custom_status', status)
                except Exception as e:
                    print(f"Error parsing XML response for {entry_name}: {e}")
                    entry_doc.db_set('docstatus', 0)
                    entry_doc.db_set('custom_api_response', f"Error parsing XML: {e}")
                    entry_doc.db_set('custom_status', 'ERROR')
            else:
                entry_doc.db_set('docstatus', 0)
                entry_doc.db_set('custom_api_response', response.text)
                entry_doc.db_set('custom_status', 'FAILED')

        except Exception as e:
            print(f"Error processing entry {entry_name}: {e}")
            # Optionally, update the entry to reflect the error state
            entry_doc.db_set('docstatus', 0)
            entry_doc.db_set('custom_api_response', str(e))
            entry_doc.db_set('custom_status', 'ERROR')


@frappe.whitelist(allow_guest=True)    
def ping():
    return "Apeksha"






 
############################### Sahayog Statement #################################################
import frappe
from frappe.utils.pdf import get_pdf
from datetime import datetime

# Pre-defined transactions dictionary
transactions_data = [
    {
        "account_number": "1234567890",
        "transaction_date": "2024-01-01",
        "amount": 1000,
        "transaction_type": "Credit",
        "description": "Salary",
        "account_type": "SAV"
    },
    {
        "account_number": "1234567890",
        "transaction_date": "2024-01-05",
        "amount": -200,
        "transaction_type": "Debit",
        "description": "Shopping",
        "account_type": "SAV"
    },
    {
        "account_number": "9876543210",
        "transaction_date": "2024-01-10",
        "amount": 1500,
        "transaction_type": "Credit",
        "description": "Freelance",
        "account_type": "RD"
        
    },
    {
        "account_number": "1234567890",
        "transaction_date": "2024-01-15",
        "amount": 1000,
        "transaction_type": "Credit",
        "description": "Electricity Bill",
        "account_type": "SAV"
    },
     {
        "account_number": "1234567890",
        "transaction_date": "2024-06-15",
        "amount": -500,
        "transaction_type": "Debit",
        "description": "Xyz",
        "account_type": "SAV"
    },
      {
        "account_number": "1234567890",
        "transaction_date": "2024-08-11",
        "amount": -200,
        "transaction_type": "Debit",
        "description": "ABC",
        "account_type": "SAV"
    },
]

@frappe.whitelist()
def fetch_transactions(account_number, start_date, end_date):
    # Convert string dates to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Filter transactions based on input
    filtered_transactions = [
        t for t in transactions_data
        if t["account_number"] == account_number
        and start_date <= datetime.strptime(t["transaction_date"], "%Y-%m-%d") <= end_date
    ]
    
    if not filtered_transactions:
        frappe.throw("No transactions found for the given criteria.")
        
    # Calculate balance for each transaction
    balance = 0  # Initialize balance
    for transaction in filtered_transactions:
        # Debit transactions are subtracted from the balance
        if transaction["transaction_type"] == "Debit":
            balance -= abs(transaction["amount"])
        # Credit transactions are added to the balance
        else:
            balance += abs(transaction["amount"])
        
        # Add the balance to the transaction object
        transaction["balance"] = balance
    
    # Render HTML for PDF
    html_content = frappe.render_template("templates/transaction_statement.html", {
        "transactions": filtered_transactions,
        "account_number": account_number,
        "start_date": start_date.strftime("%d/%m/%Y"),  # Ensure the date format is correct
        "end_date": end_date.strftime("%d/%m/%Y")  # Ensure the date format is correct
    })
    pdf_data = get_pdf(html_content)
    
    # Return PDF as response
    frappe.local.response.filename = "Transaction_Statement.pdf"
    frappe.local.response.filecontent = pdf_data
    frappe.local.response.type = "download"




# @frappe.whitelist(allow_guest=True)
# def fetch_transactions(start_date, end_date):
#     # Convert start_date and end_date to date objects for comparison
#     start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
#     end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")
    
#     # Filter transactions based on account_number and date range
#     filtered_transactions = [
#         t for t in transactions_data
#         if start_date_obj <= datetime.strptime(t["transaction_date"], "%d/%m/%Y")<= end_date_obj
#     ]
    
#     # Calculate totals for debit and credit transactions
#     total_debit = sum(abs(t["amount"]) for t in filtered_transactions if t["amount"] < 0)
#     total_credit = sum(t["amount"] for t in filtered_transactions if t["amount"] > 0)

#     # Render the HTML template with the transaction data and totals
#     html = frappe.render_template(
#         "templates/transaction_statement.html",
#         {
           
#             "start_date": start_date,
#             "end_date": end_date,
#             "transactions": filtered_transactions,
#             "total_debit": total_debit,
#             "total_credit": total_credit,
#         },
#     )

#     # Generate the PDF from the rendered HTML
#     pdf = get_pdf(html)

#     # Return the generated PDF as a response
#     frappe.local.response.filename = f"Transaction_Statement_123456789.pdf"
#     frappe.local.response.filecontent = pdf
#     frappe.local.response.type = "pdf"



###################################################################
# Database Connection Details for Statement Generation
###################################################################
import cx_Oracle


# Connection Parameters (already initialized)
username = "sahyog"
password = "sahyog"
host = "10.0.115.20"
port = "1521"  # Default port for Oracle
sid = "orcl"   # SID or service name

import cx_Oracle

def connect_to_oracle():
    """
    Connect to an Oracle database using pre-initialized parameters and perform operations
    to generate a bank statement.
    """
    # Initialize parameters
    branch_code = 'SADA15'
    ac_code = 'B110'
    ac_no = 5002355  # Replace with actual AC_NO
    acmastcode = None  # To be fetched later
    gmst_code = None  # To be fetched later

    # Create a DSN (Data Source Name)
    dsn = cx_Oracle.makedsn(host, port, service_name=sid)

    try:
        # Establish the connection
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        print("Connection successful!")

        # Create a cursor
        cursor = connection.cursor()

        # 1. Retrieve Branch Name and Branch Code
        cursor.execute("SELECT branchname, branchcode FROM sahyog.branchmas WHERE branchcode = :branch_code", {'branch_code': branch_code})
        branch_info = cursor.fetchone()
        if branch_info:
            branch_name, branch_code = branch_info
            print(f"Branch: {branch_name}, Code: {branch_code}")
        else:
            print("Branch information not found.")

        # 2. Retrieve ACMASTCODE for AC_CODE 'B110'
        cursor.execute("SELECT ACMASTCODE FROM SAHYOG.ACMAST WHERE AC_CODE = :ac_code", {'ac_code': ac_code})
        acmastcode_row = cursor.fetchone()
        if acmastcode_row:
            acmastcode = acmastcode_row[0]
            print(f"ACMASTCODE: {acmastcode}")
        else:
            print("ACMASTCODE not found.")

        # 3. Retrieve GMST_CODE using ACMASTCODE and Branch Code
        cursor.execute("SELECT gmst_code FROM SAHYOG.CURMAS WHERE ACMASTCODE = :acmastcode AND BRANCHCODE = :branch_code AND AC_NO = :ac_no", 
                       {'acmastcode': acmastcode, 'branch_code': branch_code, 'ac_no': ac_no})
        gmst_code_row = cursor.fetchone()
        if gmst_code_row:
            gmst_code = gmst_code_row[0]  # Adjust index based on the actual column order
            print(f"GMST_CODE: {gmst_code}")
        else:
            print("GMST_CODE not found.")

        # 4. Retrieve Customer Details
        cursor.execute("SELECT name, addr, city, tele, adharno, gmst_code FROM sahyog.bankmas WHERE gmst_code = :gmst_code", {'gmst_code': gmst_code})
        customer_details = cursor.fetchone()
        if customer_details:
            print("Customer Details:")
            print(f"Name: {customer_details[0]}, Address: {customer_details[1]}, City: {customer_details[2]}, Telephone: {customer_details[3]}, Aadhar No: {customer_details[4]}, GMST Code: {customer_details[5]}")
        else:
            print("Customer details not found.")

        # 5. Retrieve Transactions
        cursor.execute("SELECT tdate, drcr, csh_trn, prtcls, doc_no, debit, credit FROM SAHYOG.ACBK WHERE AC_NO = :ac_no AND FORBRANCH = :branch_code AND ACMASTCODE = :acmastcode ORDER BY TDATE", 
                       {'ac_no': ac_no, 'branch_code': branch_code, 'acmastcode': acmastcode})
        transactions = cursor.fetchall()
        print("Transactions:")
        for transaction in transactions:
            print(transaction)

    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"An error occurred: {error.message}")

    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection:
            connection.close()
            print("Connection closed.")

import cx_Oracle
import frappe
from frappe.utils.pdf import get_pdf
from datetime import datetime

@frappe.whitelist(allow_guest=True)   
def fetch_db(branch_code, ac_code, ac_no, account_type, start_date, end_date):
    try:
        # Parse dates
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Database connection parameters
        username = "sahyog"
        password = "sahyog"
        host = "10.0.115.20"
        port = "1521"
        sid = "orcl"

        # Create DSN and connect
        dsn = cx_Oracle.makedsn(host, port, service_name=sid)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT branchname FROM sahyog.branchmas WHERE branchcode = :branch_code",
            {'branch_code': branch_code}
        )
        result = cursor.fetchone()
        if not result:
            print(f"Debug: No branch found for branch_code = '{branch_code}'")
            branch_name = "Unknown Branch"
        else:
            branch_name = result[0]

        # Fetch customer details
        cursor.execute(
            """
            SELECT name, addr, city, tele, adharno FROM sahyog.bankmas
            WHERE gmst_code = (
                SELECT gmst_code FROM SAHYOG.CURMAS
                WHERE acmastcode = (
                    SELECT ACMASTCODE FROM SAHYOG.ACMAST WHERE AC_CODE = :ac_code
                )
                AND BRANCHCODE = :branch_code AND AC_NO = :ac_no
            )
            """,
            {'ac_code': ac_code, 'branch_code': branch_code, 'ac_no': ac_no}
        )
        customer_details = cursor.fetchone()
        if not customer_details:
            frappe.throw("Customer details not found.")

        customer_info = {
            "name": customer_details[0],
            "address": customer_details[1],
            "city": customer_details[2],
            "telephone": customer_details[3],
            "aadhar": customer_details[4],
        }

        # Fetch transactions within the specified period
        cursor.execute(
            """
            SELECT tdate, drcr, csh_trn, prtcls, doc_no, debit, credit
            FROM SAHYOG.ACBK
            WHERE AC_NO = :ac_no AND FORBRANCH = :branch_code AND
                  ACMASTCODE = (SELECT ACMASTCODE FROM SAHYOG.ACMAST WHERE AC_CODE = :ac_code)
                  AND tdate BETWEEN :start_date AND :end_date
            ORDER BY tdate
            """,
            {
                'ac_no': ac_no, 'branch_code': branch_code,
                'ac_code': ac_code, 'start_date': start_date, 'end_date': end_date
            }
        )
        transactions = cursor.fetchall()
        if not transactions:
            frappe.throw("No transactions found for the given criteria.")

        # Calculate opening balance by summing records before the start date
        cursor.execute(
            """
            SELECT NVL(SUM(debit), 0) - NVL(SUM(credit), 0)
            FROM SAHYOG.ACBK
            WHERE AC_NO = :ac_no AND FORBRANCH = :branch_code AND tdate < :start_date
            """,
            {'ac_no': ac_no, 'branch_code': branch_code, 'start_date': start_date}
        )
        opening_balance = cursor.fetchone()[0] or 0  # Get opening balance

        # Ensure opening balance is non-negative
        opening_balance_display = opening_balance 

        # Prepare transaction data and calculate running balance
        formatted_transactions = []
        running_balance = opening_balance  # Start with opening balance

        # Create a formatted entry for the opening balance if it is non-negative
        if opening_balance_display > 0:
            formatted_transactions.append({
                "transaction_date": start_date.strftime("%d/%m/%Y"),  # Use start_date for the opening balance
                "transaction_type": "Opening Balance",
                "description": "Opening Balance",
                "doc_no": "",
                "debit": 0.0,
                "credit": 0.0,
                "balance": running_balance,  # Opening balance
            })

        # Loop through transactions to calculate running balance
        for t in transactions:
            # Update running balance
            running_balance += t[5] - t[6]  # Debit - Credit

            formatted_transactions.append({
                "transaction_date": t[0].strftime("%d/%m/%Y"),  # Format date
                "transaction_type": "Debit" if t[5] > 0 else "Credit",
                "description": t[3],
                "doc_no": t[4],
                "debit": t[5] if t[5] > 0 else 0,  # Avoid negative
                "credit": t[6] if t[6] > 0 else 0,  # Avoid negative
                "balance": running_balance,  # Running balance
            })

        # Render PDF
        html_content = frappe.render_template("templates/transaction_statement.html", {
            "transactions": formatted_transactions,
            "branch_name": branch_name,
            "branch_code": branch_code,
            "ac_no": ac_no,
            "account_number": ac_no,
            "start_date": start_date.strftime("%d/%m/%Y"),  # Format date for display
            "end_date": end_date.strftime("%d/%m/%Y"),  # Format date for display
            "customer_info": customer_info,
            "opening_balance": opening_balance_display,  # Pass opening balance to template
        })

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
        if 'connection' in locals():
            connection.close()

