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

@frappe.whitelist()
def show_ho_logs():
    query = """
    SELECT log_type, log_time
    FROM `tabDay Management Checkin`
    WHERE branch = 'Gondia HO' AND DATE(log_time) = CURDATE();
    """
    result = frappe.db.sql(query, as_dict=True)

    if result:
        ho_log = result[0]

        # Fetch HO Day End information
        ho_day_end_query = """
        SELECT log_time
        FROM `tabDay Management Checkin`
        WHERE branch = 'Gondia HO' AND log_type = 'End' AND DATE(log_time) = CURDATE();
        """
        ho_day_end_result = frappe.db.sql(ho_day_end_query, as_dict=True)
        ho_day_end_time = ho_day_end_result[0].get("log_time").strftime('%I:%M %p') if ho_day_end_result else None
        ho_day_end_date = ho_day_end_result[0].get("log_time").strftime('%d-%m-%Y') if ho_day_end_result else None

        # Format the response based on your needs
        response = {
            "log_type": ho_log.get("log_type", ""),
            "log_time": ho_log.get("log_time", ""),
            "ho_day_start": True if ho_log.get("log_type") == "Start" else False,
            "ho_start_date": ho_log.get("log_time").strftime('%d-%m-%Y') if ho_log.get("log_time") else None,
            "ho_start_time": ho_log.get("log_time").strftime('%I:%M %p') if ho_log.get("log_time") else None,
            "ho_day_end": True if ho_day_end_result else False,
            "ho_end_date": ho_day_end_date,
            "ho_end_time": ho_day_end_time,
            # You can add more information as needed
        }
    else:
        response = {
            "ho_day_start": False,
            "ho_day_end": False,
        }

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

