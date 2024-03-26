import frappe
import pandas as pd

def read_excel_file():
    print("excel file")


def update_share_ac():

    # Fetch the first 10 Sahayog Ticket records with name from 1 to 10
    tickets = frappe.get_all(
        "Share Application",
        filters={"name": ["between", 1, 10]},
        fields=[
            "name",
            "ac_no",
            "share_ac_no",
        ],
    )

    for ticket in tickets:
        account_number = ticket.ac_no
        application_sr_no = ticket.name

        # Transfer the value of "ac_no" to "share_ac_no"
        frappe.db.set_value("Share Application", application_sr_no, "share_ac_no", account_number, update_modified=False)
        
        # Set "ac_no" to null
        frappe.db.set_value("Share Application", application_sr_no, "ac_no", None, update_modified=False)

    frappe.db.commit()
    print("\n\nUpdated share accounts\n\n")