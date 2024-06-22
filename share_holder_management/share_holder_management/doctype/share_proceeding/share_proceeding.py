# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document
from frappe.utils import now

class ShareProceeding(Document):
	pass





def get_logs(proceeding_date):
    """Fetch proceeding logs based on the given date."""
    query = """
        SELECT
            application_sr_no,
            sanction_date,
            branch,
            customer_name,
            status,
            address,
            taluka,
            city
        FROM
            `tabShare Application`
        WHERE
            sanction_date = %s;
    """

    result = frappe.db.sql(query, (proceeding_date,), as_dict=True)
    return result

def get_end_branch_details(proceeding_date):
    """Fetch proceeding logs based on the given date."""
    check_ho_end = f"""
      SELECT log_type, log_time
      FROM `tabDay Management Checkin`
     WHERE branch = 'Gondia HO' AND DATE(log_time) = '{proceeding_date}' AND log_type = 'End';
    """

    # Execute the query to check if records exist
    ho_end_records = frappe.db.sql(check_ho_end)

    # If records exist, return "Show Log"; otherwise, return "Ho not Ended"
    if ho_end_records:
        return get_logs(proceeding_date)
    else:
        frappe.throw("Ho not Ended")
  
@frappe.whitelist()
def show_proceeding_logs(proceeding_date):
    """Fetch and return proceeding logs for the given date."""
    # Define the comparison date (12th February 2024)
    comparison_date = "2024-02-12"
    
    # Check if the provided date is before 12th February 2024
    if proceeding_date < comparison_date:
        # If it is before the comparison date, fetch logs
        return get_logs(proceeding_date)
    else:
        # Otherwise, raise an exception indicating that the date is not valid
        return get_end_branch_details(proceeding_date)
        