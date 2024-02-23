# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DayManagementCheckin(Document):
	pass



def before_validate(self):
    
        # Retrieve employee_name from the "Employee" doctype
        emp_id = 1034
        emp_name = frappe.db.get_value("Employee", {"employee": emp_id}, "employee_name")
        if emp_name:
            # Set the employee_name attribute of the current object
            self.emp_name = emp_name
            frappe.throw("setting emp name")
        else:
            frappe.throw("Employee not found with ID: {0}".format(self.employee))


#modified code on 15 Feb
# @frappe.whitelist()
# def get_log_details_previous():
#     previous_day = (datetime.now() - timedelta(days=1)).date()

#     # Check if 'Start' record exists for the specified conditions on the previous day
#     start_record_exists = frappe.db.exists({
#         "doctype": "Day Management Checkin",
#         "branch": branch,
#         "log_type": log_type,
#         "log_time": ["like", f"{previous_day}%"]
#     })

#     if start_record_exists:
#         # 'Start' record exists, now check for 'End' record
#         end_record_exists = frappe.db.exists({
#             "doctype": "Day Management Checkin",
#             "branch": branch,
#             "log_type": "End",
#             "log_time": ["like", f"{previous_day}%"]
#         })

#         return end_record_exists

#     return False


@frappe.whitelist()
def get_branch_checkin_details(branch,date):
    # Get today's date and time
    # today_datetime = frappe.utils.now_datetime()

    # Query records for the current date, the specified branch, and log types 'Start' and 'End'
    start_checkin = frappe.db.sql(
        f"""SELECT branch, log_type, log_time FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'Start'""",
        (date, "Gondia HO"),
        as_dict=True,
    )

    end_checkin = frappe.db.sql(
        f"""SELECT branch, log_type, log_time FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'End'""",
        (date, "Gondia HO"),
        as_dict=True,
    )

    # Check the results and return flags
    if start_checkin and end_checkin:
        flag = "Ho Day Completed"
    elif start_checkin:
        flag = "Ho Day Started"
    elif end_checkin:
        flag = "Ho Day Ended"
    else:
        flag = "Ho Not Started"

    

    return flag




@frappe.whitelist()
def get_Ho_checkin_details(branch):
    # Get today's date and time
    today_datetime = frappe.utils.now_datetime()

    # Query records for the current date and the requested branch
    result = frappe.db.sql(
        f"""SELECT branch, log_type, log_time FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = %s""",
        (today_datetime.date(), branch),
        as_dict=True,
    )

    # Print the data using frappe.msgprint
    if result:
        msg = """
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Branch</th>
                        <th>Log Type</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
            """
        for row in result:
            log_datetime = row.get('log_time')
            log_date = log_datetime.strftime('%d/%m/%Y')
            log_time = log_datetime.strftime('%I:%M %p')

            msg += """
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                """.format(
                row.get('branch'), row.get('log_type'), log_date, log_time
            )
        msg += """
                </tbody>
            </table>
            """
        frappe.msgprint(msg)
    else:
        frappe.msgprint("No checkin details found for {} on {}".format(branch, today_datetime.date()))

    return result


@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()


@frappe.whitelist()
def ho_day_start_and_end(branch,date):
    # Get today's date and time
    # today_datetime = frappe.utils.now_datetime()

    # Query records for the current date, the specified branch, and log types 'Start' and 'End'
    day = frappe.db.sql(
        f"""SELECT log_type, log_time FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = %s""",
        (date, "Gondia HO"),
        as_dict=True,
    )

    # HTML string for the table
    html_table = "<table border='1'>"

    # Add header row
    html_table += "<tr><th>Log Type</th><th>Log Time</th></tr>"

    # Add rows for each record
    if day:
        for record in day:
            html_table += f"<tr><td>{record.get('log_type')}</td><td>{record.get('log_time')}</td></tr>"
    else:
        # Add a row indicating no records found
        html_table += "<tr><td colspan='2'>No records found</td></tr>"

    # Close the table tag
    html_table += "</table>"

  

       # Check if records are found with 'Start' and 'End' log types
    start_found = any(record['log_type'] == 'Start' for record in day)
    end_found = any(record['log_type'] == 'End' for record in day)

    # Determine the flag
    if start_found and end_found:
        flag = "Day Completed"
    elif start_found:
        flag = "Day Not Ended"
    else:
        flag = "Day Not Started"

    return flag


@frappe.whitelist()
def branch_day_start_and_end(branch,date):
    # Get today's date and time
    # today_datetime = frappe.utils.now_datetime()

    # Query records for the current date, the specified branch, and log types 'Start' and 'End'
    day = frappe.db.sql(
        f"""SELECT log_type, log_time FROM `tabDay Management Checkin`
            WHERE DATE(log_time) = %s AND branch = %s""",
        (date, branch),
        as_dict=True,
    )
    


    # HTML string for the table
    html_table = "<table border='1'>"

    # Add header row
    html_table += "<tr><th>Log Type</th><th>Log Time</th></tr>"

    # Add rows for each record
    if day:
        for record in day:
            html_table += f"<tr><td>{record.get('log_type')}</td><td>{record.get('log_time')}</td></tr>"
    else:
        # Add a row indicating no records found
        html_table += "<tr><td colspan='2'>No records found</td></tr>"

    # Close the table tag
    html_table += "</table>"

  

       # Check if records are found with 'Start' and 'End' log types
    start_found = any(record['log_type'] == 'Start' for record in day)
    end_found = any(record['log_type'] == 'End' for record in day)
    

    # Determine the flag
    if start_found and end_found:
        flag = "Day Completed"
    #elif check_branch_day_end:
        #flag = "You Can End HO"
    elif start_found:
        flag = "Day Not Ended"
    else:
        flag = "Day Not Started"

    return flag

    

#before save check all branches are ended or not.
@frappe.whitelist()
def start_end_details(totalEndCount, totalBranchCount):
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

    # Check if counts match
    if total_end_result[0]['total_end_count'] == branches_result[0]['total_branch_count']:
        return {
            'message': 'Success',
            'flag': True,
            'totalEndCount': total_end_result[0]['total_end_count'],
            'totalBranchCount': branches_result[0]['total_branch_count'],
        }
    else:
        return {
            'message': 'Counts do not match',
            'flag': False,
            'totalEndCount': total_end_result[0]['total_end_count'],
            'totalBranchCount': branches_result[0]['total_branch_count'],
        }  