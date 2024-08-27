# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import now
from datetime import datetime
from frappe import _
from datetime import timedelta


class DayManagement(Document):
    pass


# get current date-time of server
@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()


# fetching details of Gondia HO logs in day management (showing data in cards)
@frappe.whitelist()
def show_ho_logs(date):
    start_query = """
    SELECT log_type, log_time
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = %s AND log_type = 'Start' AND branch = 'Gondia HO';
    """
    start_result = frappe.db.sql(start_query, (date,), as_dict=True)

    end_query = """
    SELECT log_type, log_time
    FROM `tabDay Management Checkin`
    WHERE branch = 'Gondia HO' AND DATE(log_time) =%s  AND log_type = 'End';
    """
    end_result = frappe.db.sql(end_query, (date,), as_dict=True)

    total_start_query = """
    SELECT COUNT(*) AS total_start_count
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = %s AND log_type = 'Start' AND branch != 'Gondia HO';
    """
    total_start_result = frappe.db.sql(total_start_query, (date,), as_dict=True)

    total_end_query = """
    SELECT COUNT(*) AS total_end_count
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = %s AND log_type = 'End' AND branch != 'Gondia HO';
    """
    total_end_result = frappe.db.sql(total_end_query, (date,), as_dict=True)

    branches_query = """
    SELECT COUNT(DISTINCT branch) AS total_branch_count
    FROM `tabUser`
    WHERE role_profile_name = 'Share User Employee';
    """
    branches_result = frappe.db.sql(branches_query, as_dict=True)

    response = {
        "start_details": False,
        "end_details": False,
        "total_start_count": 0,
        "total_end_count": 0,
        "total_branch_count": 0,
    }

    if start_result:
        ho_start_log = start_result[0]
        response["start_details"] = {
            "log_type": ho_start_log.get("log_type", ""),
            "log_time": ho_start_log.get("log_time", ""),
            "ho_start_date": (
                ho_start_log.get("log_time").strftime("%d-%m-%Y")
                if ho_start_log.get("log_time")
                else None
            ),
            "ho_start_time": (
                ho_start_log.get("log_time").strftime("%I:%M %p")
                if ho_start_log.get("log_time")
                else None
            ),
        }

    if end_result:
        ho_end_log = end_result[0]
        response["end_details"] = {
            "log_type": ho_end_log.get("log_type", ""),
            "log_time": ho_end_log.get("log_time", ""),
            "ho_end_date": (
                ho_end_log.get("log_time").strftime("%d-%m-%Y")
                if ho_end_log.get("log_time")
                else None
            ),
            "ho_end_time": (
                ho_end_log.get("log_time").strftime("%I:%M %p")
                if ho_end_log.get("log_time")
                else None
            ),
        }

    if total_start_result:
        response["total_start_count"] = total_start_result[0].get(
            "total_start_count", 0
        )

    if total_end_result:
        response["total_end_count"] = total_end_result[0].get("total_end_count", 0)

    if branches_result:
        response["total_branch_count"] = branches_result[0].get("total_branch_count", 0)

    return response


# original code for fetching details of branches log
# @frappe.whitelist()
# def show_branch_logs():
#     # Fetch data using Frappe database query
#     query = """
#         SELECT
#         u.branch,
#         MAX(CASE WHEN d.log_type = 'start' THEN d.log_time END) AS start_time,
#         MAX(CASE WHEN d.log_type = 'start' THEN 'start' END) AS start_log_type,
#         MAX(CASE WHEN d.log_type = 'end' THEN d.log_time END) AS end_time,
#         MAX(CASE WHEN d.log_type = 'end' THEN 'end' END) AS end_log_type,
#         MAX(CASE WHEN d.log_type = 'start' THEN d.employee END) AS Day_Start_by,
#         MAX(CASE WHEN d.log_type = 'end' THEN d.employee_name END) AS Day_End_by
#     FROM (
#        SELECT DISTINCT branch
#        FROM `tabUser`
#        WHERE role_profile_name = 'Share User Employee'
#     ) u
#     LEFT JOIN `tabDay Management Checkin` d ON u.branch = d.branch AND DATE(d.log_time) = CURDATE()
#     GROUP BY u.branch
#     ORDER BY start_log_type DESC;
#     """

#     result = frappe.db.sql(query, as_dict=True)

#     return {
#         "result": result
#     }


# modified code for fetching details of branches log (showing data of branches in table form)
@frappe.whitelist()
def show_branch_logs(date):
    # Fetch data using Frappe database query
    query = """
        SELECT
            u.branch,
            MAX(CASE WHEN d.log_type = 'start' THEN d.log_time END) AS start_time,
            MAX(CASE WHEN d.log_type = 'start' THEN 'start' END) AS start_log_type,
            MAX(CASE WHEN d.log_type = 'end' THEN d.log_time END) AS end_time,
            MAX(CASE WHEN d.log_type = 'end' THEN 'end' END) AS end_log_type,
            MAX(CASE WHEN d.log_type = 'start' THEN e.employee_name END) AS Day_Start_by,
            MAX(CASE WHEN d.log_type = 'end' THEN e.employee_name END) AS Day_End_by
        FROM (
           SELECT DISTINCT branch
           FROM `tabUser`
           WHERE role_profile_name = 'Share User Employee'
        ) u
        LEFT JOIN `tabDay Management Checkin` d ON u.branch = d.branch AND DATE(d.log_time) = %s
        LEFT JOIN `tabEmployee` e ON d.employee = e.name
        GROUP BY u.branch
        ORDER BY start_log_type DESC;
    """

    result = frappe.db.sql(query, (date,), as_dict=True)

    return {"result": result}


from frappe.utils import now

# #to start branch from HO executive
# @frappe.whitelist()
# def start_branch_day(branch,datetime,userId,employeeName):
#     try:

#         # Create a new document
#         doc = frappe.new_doc('Day Management Checkin')
#         doc.log_type = 'Start'
#         doc.branch = branch
#         doc.log_time = datetime
#         doc.employee = userId
#         doc.emp_name=employeeName

#         try:
#             doc.insert()
#             # Log success to the console
#             print(f"Branch day started successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}")
#             return True

#         except frappe.DuplicateEntryError:
#             print(f"Document for {branch} by user {userId} already exists")
#             return False


#     except Exception as e:
#         # Log error to the console
#         print(f"Error starting branch day for {branch} by user {userId}: {str(e)}")
#         frappe.throw(str(e))

# Modified above code for date format
from datetime import datetime


# To start Day of HO
@frappe.whitelist()
def start_HO_day(branch, datetime_str, userId, employeeName):
    try:
        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

        # Create a new document
        doc = frappe.new_doc("Day Management Checkin")
        doc.log_type = "Start"
        doc.branch = branch
        doc.log_time = datetime_obj
        doc.employee = userId
        doc.emp_name = employeeName

        try:
            doc.insert()
            # Log success to the console
            print(
                f"HO day started successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}"
            )
            return True

        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False

    except Exception as e:
        # Log error to the console
        print(f"Error starting branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


# To end Day of HO
@frappe.whitelist()
def end_HO_day(branch, datetime_str, userId, employeeName):
    try:
        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

        # Create a new document
        doc = frappe.new_doc("Day Management Checkin")
        doc.log_type = "End"
        doc.branch = branch
        doc.log_time = datetime_obj
        doc.employee = userId
        doc.emp_name = employeeName

        try:
            doc.insert()
            # Log success to the console
            print(
                f"HO day ended successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}"
            )
            return True

        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False

    except Exception as e:
        # Log error to the console
        print(f"Error ending branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


@frappe.whitelist()
def start_branch_day(branch, datetime_str, userId, employeeName):
    try:
        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y,%H:%M")

        # Create a new document
        doc = frappe.new_doc("Day Management Checkin")
        doc.log_type = "Start"
        doc.branch = branch
        doc.log_time = datetime_obj
        doc.employee = userId
        doc.emp_name = employeeName

        try:
            doc.insert()
            # Log success to the console
            print(
                f"Branch day started successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}"
            )
            return True

        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False

    except Exception as e:
        # Log error to the console
        print(f"Error starting branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


# to end branch from HO executive
@frappe.whitelist()
def end_branch_day(branch, datetime_str, userId, employeeName):
    try:
        # Convert datetime string to datetime object
        datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y,%H:%M")

        # Create a new document
        doc = frappe.new_doc("Day Management Checkin")
        doc.log_type = "End"
        doc.branch = branch
        doc.log_time = datetime_obj
        doc.employee = userId
        doc.emp_name = employeeName

        try:
            doc.insert()
            # Log success to the console
            print(
                f"Branch day ended successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}"
            )
            return True

        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False

    except Exception as e:
        # Log error to the console
        print(f"Error ending branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


@frappe.whitelist()
def delete_end_record(branch, endLogType, endTime):
    try:
        # Find the document by matching branch, endLogType, and endTime
        doc_name = f"{branch}/{endTime}/{endLogType}"  # Constructing document name
        doc = frappe.get_doc("Day Management Checkin", doc_name)

        # Check if the document exists
        if doc:
            # Delete the document
            doc.delete()

            # Log success
            # frappe.msgprint("Record deleted successfully")
            return True
        else:
            # Document not found
            # frappe.msgprint("No end record found for this branch")
            return False

    except frappe.DoesNotExistError:
        # Document not found
        # frappe.msgprint("No end record found for this branch")
        return False

    except Exception as e:
        # Log error
        frappe.msgprint(f"Error deleting end record: {str(e)}")
        return False


# #optimization of above code
from datetime import timedelta


# Fetching Last Five REcords from today_datetime
# Check conditions for each date in the specified range
@frappe.whitelist()
def check_conditions():
    # Set the target date as '2024-02-20'
    # today_datetime_str = '2024-02-20'
    # today_datetime = datetime.strptime(today_datetime_str, '%Y-%m-%d')
    # date_range = [today_datetime - timedelta(days=i) for i in range(4, -1, -1)]

    today_datetime_str = get_server_datetime().strftime("%Y-%m-%d %H:%M:%S")
    today_datetime = datetime.strptime(today_datetime_str, "%Y-%m-%d %H:%M:%S")
    date_range = [today_datetime - timedelta(days=i) for i in range(6, -1, -1)]

    results = []

    for date in date_range:
        # Retrieve counts for different log types and branches for the specified date
        log_count = get_log_status(date)
        ho_start_count = get_ho_start_status(date)
        total_start_count = get_total_branch_start_status(date)
        total_branch_count = get_total_branch_status()
        total_end_count = get_total_branch_end_status(date)
        ho_end_count = get_ho_end_status(date)

        # Check if all data is false in one row
        all_false_values = all(
            [
                log_count == 0,
                ho_start_count == 0,
                total_start_count != total_branch_count,
                total_end_count != total_branch_count,
                ho_end_count == 0,
            ]
        )

        # Check if all specified conditions are true for the current date
        all_true_values = all(
            [
                log_count > 0,
                ho_start_count > 0,
                total_start_count == total_branch_count,
                total_end_count == total_branch_count,
                ho_end_count > 0,
            ]
        )

        # Skip adding the "Previous Day" row to the results
        if all_true_values:
            results.append(
                {
                    "Status": "Previous Day",
                    "Date": date.date(),
                    "HO Day Start": ho_start_count > 0,
                    "All Branch Day Start": total_start_count == total_branch_count,
                    "All Branch Day End": total_end_count == total_branch_count,
                    "HO Day End": ho_end_count > 0,
                }
            )
        elif any(
            [
                log_count > 0,
                ho_start_count > 0,
                total_start_count == total_branch_count,
                total_end_count == total_branch_count,
                ho_end_count > 0,
            ]
        ):
            results.append(
                {
                    "Status": "Current Day",
                    "Date": date.date(),
                    "HO Day Start": ho_start_count > 0,
                    "All Branch Day Start": total_start_count == total_branch_count,
                    "All Branch Day End": total_end_count == total_branch_count,
                    "HO Day End": ho_end_count > 0,
                }
            )
        elif (
            not all_false_values
        ):  # Add this condition to check if all records are false
            results.append(
                {
                    "Status": "No Records",
                    "Date": date.date(),
                    "HO Day Start": ho_start_count > 0,
                    "All Branch Day Start": total_start_count == total_branch_count,
                    "All Branch Day End": total_end_count == total_branch_count,
                    "HO Day End": ho_end_count > 0,
                }
            )

    # Filter out the "Previous Day" status row from the results
    results = [result for result in results if result.get("Status") != "Previous Day"]

    # If no records found, append the current date with a special flag
    if not results:
        results.append(
            {
                "Status": "No Records",
                "Date": today_datetime.date(),  # Use the current date
                "CurrentDateFlag": True,  # Add a flag to indicate the current date
            }
        )

    return results


# Get the status of log entries for a specific date
def get_log_status(date):
    query = """
        SELECT COUNT(*) AS log_count
        FROM `tabDay Management Checkin`
        WHERE DATE(log_time) = %s;
    """
    result = frappe.db.sql(query, (date.date(),), as_dict=True)
    return result[0].get("log_count", 0)


# Get the status of HO (Gondia HO) start entry for a specific date , it will return True/False
def get_ho_start_status(date):
    query = """
        SELECT COUNT(*) AS ho_start_count
        FROM `tabDay Management Checkin`
        WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'Start';
    """
    result = frappe.db.sql(query, (date.date(),), as_dict=True)
    return result[0].get("ho_start_count", 0)


# Get the status of total start entries (excluding Gondia HO) for a specific date
def get_total_branch_start_status(date):
    query = """
        SELECT COUNT(*) AS total_start_count
        FROM `tabDay Management Checkin`
        WHERE DATE(log_time) = %s AND log_type = 'Start' AND branch != 'Gondia HO';
    """
    result = frappe.db.sql(query, (date.date(),), as_dict=True)
    return result[0].get("total_start_count", 0)


# Get the status of distinct branches that have the role profile 'Share User Employee'
def get_total_branch_status():
    query = """
        SELECT COUNT(DISTINCT branch) AS total_branch_count
        FROM `tabUser`
        WHERE role_profile_name = 'Share User Employee';
    """
    result = frappe.db.sql(query, as_dict=True)
    return result[0].get("total_branch_count", 0)


# Get the status of total end entries (excluding Gondia HO) for a specific date
def get_total_branch_end_status(date):
    query = """
        SELECT COUNT(*) AS total_end_count
        FROM `tabDay Management Checkin`
        WHERE DATE(log_time) = %s AND log_type = 'End' AND branch != 'Gondia HO';
    """
    result = frappe.db.sql(query, (date.date(),), as_dict=True)
    return result[0].get("total_end_count", 0)


# Get the count of HO (Gondia HO) end entries for a specific date
def get_ho_end_status(date):
    query = """
        SELECT COUNT(*) AS ho_end_count
        FROM `tabDay Management Checkin`
        WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'End';
    """
    result = frappe.db.sql(query, (date.date(),), as_dict=True)
    return result[0].get("ho_end_count", 0)
