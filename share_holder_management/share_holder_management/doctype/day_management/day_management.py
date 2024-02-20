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

@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()

@frappe.whitelist()
def start_branch_day(branch, userId,employeeName):
    try:
        # Import the now function from frappe.utils
        from frappe.utils import now
        
        # Create a new document
        doc = frappe.new_doc('Day Management Checkin')
        doc.log_type = 'Start'
        doc.branch = branch
        doc.log_time = now()
        doc.employee = userId
        doc.emp_name=employeeName

        try:
            doc.insert()
            # Log success to the console
            print(f"Branch day started successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}")
            return True
        
        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False


    except Exception as e:
        # Log error to the console
        print(f"Error starting branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


@frappe.whitelist()
def end_branch_day(branch, userId, employeeName):
    try:
        

        # Create a new document
        doc = frappe.new_doc('Day Management Checkin')
        doc.log_type = 'End'
        doc.branch = branch
        doc.log_time = now()
        doc.employee = userId
        doc.emp_name = employeeName

        try:
            doc.insert()
            # Log success to the console
            print(f"Branch day ended successfully for {branch} by user {userId}, Employee Name: {doc.emp_name}")
            return True

        except frappe.DuplicateEntryError:
            print(f"Document for {branch} by user {userId} already exists")
            return False


    except Exception as e:
        # Log error to the console
        print(f"Error ending branch day for {branch} by user {userId}: {str(e)}")
        frappe.throw(str(e))


#original code for fetching details of branches log
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

#modified code for detching employee data
@frappe.whitelist()
def show_branch_logs():
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
        LEFT JOIN `tabDay Management Checkin` d ON u.branch = d.branch AND DATE(d.log_time) = CURDATE()
        LEFT JOIN `tabEmployee` e ON d.employee = e.name
        GROUP BY u.branch
        ORDER BY start_log_type DESC;
    """

    result = frappe.db.sql(query, as_dict=True)

    return {
        "result": result
    }


#new code added here
@frappe.whitelist()
def show_ho_logs():
    start_query = """
    SELECT log_type, log_time
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = CURDATE() AND log_type = 'Start' AND branch = 'Gondia HO';
    """
    start_result = frappe.db.sql(start_query, as_dict=True)

    end_query = """
    SELECT log_type, log_time
    FROM `tabDay Management Checkin`
    WHERE branch = 'Gondia HO' AND DATE(log_time) = CURDATE() AND log_type = 'End';
    """
    end_result = frappe.db.sql(end_query, as_dict=True)

    total_start_query = """
    SELECT COUNT(*) AS total_start_count
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = CURDATE() AND log_type = 'Start' AND branch != 'Gondia HO';
    """
    total_start_result = frappe.db.sql(total_start_query, as_dict=True)

    total_end_query = """
    SELECT COUNT(*) AS total_end_count
    FROM `tabDay Management Checkin`
    WHERE DATE(log_time) = CURDATE() AND log_type = 'End' AND branch != 'Gondia HO';
    """
    total_end_result = frappe.db.sql(total_end_query, as_dict=True)

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
            "ho_start_date": ho_start_log.get("log_time").strftime('%d-%m-%Y') if ho_start_log.get("log_time") else None,
            "ho_start_time": ho_start_log.get("log_time").strftime('%I:%M %p') if ho_start_log.get("log_time") else None,
        }

    if end_result:
        ho_end_log = end_result[0]
        response["end_details"] = {
            "log_type": ho_end_log.get("log_type", ""),
            "log_time": ho_end_log.get("log_time", ""),
            "ho_end_date": ho_end_log.get("log_time").strftime('%d-%m-%Y') if ho_end_log.get("log_time") else None,
            "ho_end_time": ho_end_log.get("log_time").strftime('%I:%M %p') if ho_end_log.get("log_time") else None,
        }

    if total_start_result:
        response["total_start_count"] = total_start_result[0].get("total_start_count", 0)

    if total_end_result:
        response["total_end_count"] = total_end_result[0].get("total_end_count", 0)

    if branches_result:
        response["total_branch_count"] = branches_result[0].get("total_branch_count", 0)

    return response


# @frappe.whitelist()
# def get_server_datetime():
#     return frappe.utils.now_datetime()

# @frappe.whitelist()
# def Previous_Day():
#     return
#     Current_date = get_server_datetime()




# @frappe.whitelist()
# def Current_Day():
#     return



@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()

# @frappe.whitelist()
# def check_conditions():
    # today_datetime = get_server_datetime()
    # previous_day = today_datetime - timedelta(days=1)

#     # Calculate the previous day
#     previous_day = today_datetime - timedelta(days=1)

#     # 1. Check if there is a record for the previous day
#     previous_day_query = """
#         SELECT COUNT(*) AS previous_day_count
#         FROM `tabDay Management Checkin`
#         WHERE DATE(log_time) = %s;
#     """
#     previous_day_result = frappe.db.sql(previous_day_query, (previous_day.date(),), as_dict=True)
#     previous_day_count = previous_day_result[0].get('previous_day_count', 0)

#     # 2. Check if there is an "Start" log entry for Gondia HO on the previous day
#     ho_start_query = """
#         SELECT COUNT(*) AS ho_start_count
#         FROM `tabDay Management Checkin`
#         WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'Start';
#     """
#     ho_start_result = frappe.db.sql(ho_start_query, (previous_day.date(),), as_dict=True)
#     ho_start_count = ho_start_result[0].get('ho_start_count', 0)

#     # 3. Check if the total count of "Start" log entries for all branches equals the total number of branches
#     total_start_query = """
#         SELECT COUNT(*) AS total_start_count
#         FROM `tabDay Management Checkin`
#         WHERE DATE(log_time) = CURDATE() AND log_type = 'Start' AND branch != 'Gondia HO';
#     """
#     total_start_result = frappe.db.sql(total_start_query, as_dict=True)
#     total_start_count = total_start_result[0].get('total_start_count', 0)

#     branches_query = """
#         SELECT COUNT(DISTINCT branch) AS total_branch_count
#         FROM `tabUser`
#         WHERE role_profile_name = 'Share User Employee';
#     """
#     branches_result = frappe.db.sql(branches_query, as_dict=True)
#     total_branch_count = branches_result[0].get('total_branch_count', 0)

#     # 4. Check if the total count of "End" log entries for all branches equals the total number of branches
#     total_end_query = """
#         SELECT COUNT(*) AS total_end_count
#         FROM `tabDay Management Checkin`
#         WHERE DATE(log_time) = CURDATE() AND log_type = 'End' AND branch != 'Gondia HO';
#     """
#     total_end_result = frappe.db.sql(total_end_query, as_dict=True)
#     total_end_count = total_end_result[0].get('total_end_count', 0)

#     # 5. Check if there is an "End" log entry for Gondia HO on the previous day
#     ho_end_query = """
#         SELECT COUNT(*) AS ho_end_count
#         FROM `tabDay Management Checkin`
#         WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'End';
#     """
#     ho_end_result = frappe.db.sql(ho_end_query, (previous_day.date(),), as_dict=True)
#     ho_end_count = ho_end_result[0].get('ho_end_count', 0)

    
    
#     # Return True or False based on conditions
#     return {
#         "Status": True if previous_day_count > 0 else False,
#         "Date": previous_day.date(),
#         "HO Day Start": True if ho_start_count > 0 else False,
#         "All Branch Day Start": True if total_start_count == total_branch_count else False,
#         "All Branch Day End": True if total_end_count == total_branch_count else False,
#         "HO Day End": True if ho_end_count > 0 else False,
#     }

from datetime import timedelta


#Fetching Last Five REcords from today_datetime
@frappe.whitelist()
def check_conditions():
    today_datetime_str = '2024-02-17'

    # Convert the string to a datetime object
    today_datetime = datetime.strptime(today_datetime_str, '%Y-%m-%d')

    # Create a list of the last five dates
    date_range = [today_datetime - timedelta(days=i) for i in range(4, -1, -1)]

    results = []
    for date in date_range:
        # Check if there is a record for the current date
        query = """
            SELECT COUNT(*) AS log_count
            FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s;
        """
        result = frappe.db.sql(query, (date.date(),), as_dict=True)
        log_count = result[0].get('log_count', 0)

        # Check if there is a "Start" log entry for Gondia HO on the current date
        ho_start_query = """
            SELECT COUNT(*) AS ho_start_count
            FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'Start';
        """
        ho_start_result = frappe.db.sql(ho_start_query, (date.date(),), as_dict=True)
        ho_start_count = ho_start_result[0].get('ho_start_count', 0)

        # Check if the total count of "Start" log entries for all branches equals the total number of branches
        total_start_query = """
            SELECT COUNT(*) AS total_start_count
            FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND log_type = 'Start' AND branch != 'Gondia HO';
        """
        total_start_result = frappe.db.sql(total_start_query, (date.date(),), as_dict=True)
        total_start_count = total_start_result[0].get('total_start_count', 0)

        branches_query = """
            SELECT COUNT(DISTINCT branch) AS total_branch_count
            FROM `tabUser`
            WHERE role_profile_name = 'Share User Employee';
        """
        branches_result = frappe.db.sql(branches_query, as_dict=True)
        total_branch_count = branches_result[0].get('total_branch_count', 0)

        # Check if the total count of "End" log entries for all branches equals the total number of branches
        total_end_query = """
            SELECT COUNT(*) AS total_end_count
            FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND log_type = 'End' AND branch != 'Gondia HO';
        """
        total_end_result = frappe.db.sql(total_end_query, (date.date(),), as_dict=True)
        total_end_count = total_end_result[0].get('total_end_count', 0)

        # Check if there is an "End" log entry for Gondia HO on the current date
        ho_end_query = """
            SELECT COUNT(*) AS ho_end_count
            FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = 'Gondia HO' AND log_type = 'End';
        """
        ho_end_result = frappe.db.sql(ho_end_query, (date.date(),), as_dict=True)
        ho_end_count = ho_end_result[0].get('ho_end_count', 0)

        # Check if there is at least one True value in any of the columns
        has_true_value = any([
            log_count > 0,
            ho_start_count > 0,
            total_start_count == total_branch_count,
            total_end_count == total_branch_count,
            ho_end_count > 0,
        ])

        # Append the result for the current date to the results list only if status is "Record Present"
        if has_true_value:
            results.append({
                "Status": "Record Present",
                "Date": date.date(),
                "HO Day Start": True if ho_start_count > 0 else False,
                "All Branch Day Start": True if total_start_count == total_branch_count else False,
                "All Branch Day End": True if total_end_count == total_branch_count else False,
                "HO Day End": True if ho_end_count > 0 else False,
            })


    return results


