import frappe
from frappe.utils import now
from frappe.utils.data import now_datetime
import openpyxl as pxl
import pandas as pd


@frappe.whitelist()
def load_items():
    SOURCE = "/files/Employee.xlsx"  # Replace with the correct file path
    try:
        # Load workbook and save it (this is a workaround)
        wkbk = pxl.load_workbook(SOURCE)
        wkbk.save(SOURCE)

        # Read Excel file using pandas
        df = pd.read_excel(SOURCE)

        # Print data in table format
        print(df.to_string(index=False))

        # Optional: Save data to Frappe database
        # Assuming you have a doctype named 'Excel Data' with fields matching columns in the Excel file
        # for index, row in df.iterrows():
        #     frappe.get_doc({
        #         "doctype": "Excel Data",
        #         "field1": row['Column1'],
        #         "field2": row['Column2'],
        #         # Add more fields as needed
        #     }).insert()

    except Exception as e:
        print(f"Error reading Excel file: {e}")


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
