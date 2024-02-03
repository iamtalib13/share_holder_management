# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class DayManagement(Document):
    pass

@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()

# @frappe.whitelist()
# def show_branch_logs(self):
#     result = frappe.db.sql(
#         f"""SELECT
#                 u.branch,
#                 MAX(CASE WHEN d.log_type = 'start' THEN d.log_time END) AS start_time,
#                 MAX(CASE WHEN d.log_type = 'start' THEN 'start' END) AS start_log_type,
#                 MAX(CASE WHEN d.log_type = 'end' THEN d.log_time END) AS end_time,
#                 MAX(CASE WHEN d.log_type = 'end' THEN 'end' END) AS end_log_type
#             FROM (
#                 SELECT DISTINCT branch
#                 FROM `tabUser`
#                 WHERE role_profile_name = 'Share User Employee'
#             ) u
#             LEFT JOIN `tabDay Management Checkin` d ON u.branch = d.branch AND DATE(d.log_time) = CURDATE()
#             GROUP BY u.branch;""",
#         as_dict=True
#     )

#     if result:
#         return result
#     else:
#         frappe.msgprint("Error fetching branch logs")
#         return []


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
        MAX(CASE WHEN d.log_type = 'start' THEN d.employee_name END) AS Day_Start_by,
        MAX(CASE WHEN d.log_type = 'end' THEN d.employee_name END) AS Day_End_by
    FROM (
       SELECT DISTINCT branch
       FROM `tabUser`
       WHERE role_profile_name = 'Share User Employee'
    ) u
    LEFT JOIN `tabDay Management Checkin` d ON u.branch = d.branch AND DATE(d.log_time) = CURDATE()
    GROUP BY u.branch
    ORDER BY start_log_type DESC;
    """

    result = frappe.db.sql(query, as_dict=True)

    return {
        "result": result
    }

# @frappe.whitelist()
# def show_ho_logs():
#     query = """
#     SELECT log_type, log_time
#     FROM `tabDay Management Checkin`
#     WHERE branch = 'Gondia HO' AND DATE(log_time) = CURDATE();
#     """
#     result = frappe.db.sql(query, as_dict=True)

#     if result:
#         ho_log = result[0]

#         # Format the response based on your needs
#         response = {
#             "log_type": ho_log.get("log_type", ""),
#             "log_time": ho_log.get("log_time", ""),
#             "ho_day_start": True if ho_log.get("log_type") == "Start" else False,
#             "ho_start_date": ho_log.get("log_time").strftime('%d-%m-%Y') if ho_log.get("log_time") else None,
#             "ho_start_time": ho_log.get("log_time").strftime('%I:%M %p') if ho_log.get("log_time") else None,
#             # You can add more information as needed
#         }
#     else:
#         response = {
#             "ho_day_start": False,
#         }

#     return response

# @frappe.whitelist()
# def show_ho_logs():
#     query = """
#     SELECT log_type, log_time
#     FROM `tabDay Management Checkin`
#     WHERE branch = 'Gondia HO' AND DATE(log_time) = CURDATE();
#     """
#     result = frappe.db.sql(query, as_dict=True)

#     if result:
#         ho_log = result[0]

#         # Fetch HO Day End information
#         ho_day_end_query = """
#         SELECT log_time
#         FROM `tabDay Management Checkin`
#         WHERE branch = 'Gondia HO' AND log_type = 'End' AND DATE(log_time) = CURDATE();
#         """
#         ho_day_end_result = frappe.db.sql(ho_day_end_query, as_dict=True)
#         ho_day_end_time = ho_day_end_result[0].get("log_time").strftime('%I:%M %p') if ho_day_end_result else None
#         ho_day_end_date = ho_day_end_result[0].get("log_time").strftime('%d-%m-%Y') if ho_day_end_result else None

#         # Format the response based on your needs
#         response = {
#             "log_type": ho_log.get("log_type", ""),
#             "log_time": ho_log.get("log_time", ""),
#             "ho_day_start": True if ho_log.get("log_type") == "Start" else False,
#             "ho_start_date": ho_log.get("log_time").strftime('%d-%m-%Y') if ho_log.get("log_time") else None,
#             "ho_start_time": ho_log.get("log_time").strftime('%I:%M %p') if ho_log.get("log_time") else None,
#             "ho_day_end": True if ho_day_end_result else False,
#             "ho_end_date": ho_day_end_date,
#             "ho_end_time": ho_day_end_time,
#             # You can add more information as needed
#         }
#     else:
#         response = {
#             "ho_day_start": False,
#             "ho_day_end": False,
#         }

#     return response

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
# def start_ho_day(docname):
#     # Fetch the document
#     doc = frappe.get_doc("Day Management Checkin", docname)

#     # Update the necessary fields to indicate that HO day has started
#     doc.ho_day_start = True
#     doc.save()

#     # You can add more logic here if needed

#     return "HO Day Started Successfully"


