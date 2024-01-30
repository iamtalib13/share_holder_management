import frappe

def cron():
    tickets = frappe.get_all(
        "Share Application",
        filters={"status": "update"},
        fields=["name", "ac_no", "share_ac_no","status"],
        order_by="modified DESC"
    )

    for ticket in tickets:
        account_number = ticket.ac_no
        application_sr_no = ticket.name 

        # Transfer the value of "ac_no" to "share_ac_no"
        frappe.db.set_value("Share Application", application_sr_no, "share_ac_no", account_number, update_modified=False)
        
        # Set "ac_no" to null
        frappe.db.set_value("Share Application", application_sr_no, "ac_no", None, update_modified=False)

    frappe.db.commit()  # Commit changes after updating all records

    print("\n\nUpdated share accounts where status is 'update'\n\n")
