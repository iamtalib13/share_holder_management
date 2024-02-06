# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ShareProceeding(Document):
	pass

@frappe.whitelist()
def show_proceeding_logs(proceeding_date):
    # Fetch data using Frappe database query
    query = """
        SELECT
            application_sr_no,
            sanction_date,
            branch,
            customer_name
        FROM
            `tabShare Application`
        WHERE
            application_date = %s;
    """

    result = frappe.db.sql(query, (proceeding_date,), as_dict=True)
    return result