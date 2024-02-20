import frappe
from frappe.utils import now


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
        frappe.db.set_value("Share Test", id, "start_range", start_range, update_modified=False)
        frappe.db.set_value("Share Test", id, "end_range", end_range, update_modified=False)

        # Update last_end_range for the next iteration
        last_end_range = end_range

    frappe.db.commit()  # Commit changes after updating all records

    print("\n\nUpdated range '\n\n")
def update():
    batch_size = 30000  # Adjust the batch size as needed
    total_records = 333514
    processed_records = 0

    while processed_records < total_records:
        tickets = frappe.get_all(
            "Share Application",
            filters={"status": "Draft"},
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
                frappe.db.set_value("Share Application", id, "status", "Sanctioned", update_modified=False)
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

def day_end():
    try:
        # Fetch distinct branches from the database
        result_branches = frappe.db.sql("""
            SELECT DISTINCT branch
            FROM `tabUser`
            WHERE role_profile_name = 'Share User Employee'
        """, as_dict=True)

        if result_branches:
            print("\nCreating Day End Documents:")

            # Loop through each branch and create a Day Management Checkin document
            for branch in result_branches:
                # create a new document
                doc = frappe.new_doc('Day Management Checkin')
                doc.branch = branch.get('branch')
                doc.status = "Sanctioned"
                doc.log_type = "End"
                doc.log_time = now()

                try:
                    doc.insert()
                    print(f"Created Day End Document for Branch {branch.get('branch')}")
                except frappe.DuplicateEntryError:
                    print(f"Day End for Branch {branch.get('branch')} already exists.")

        else:
            print("\nNo branches found for day end")

    except Exception as e:
        print(f"Error: {e}")
        
        
def day_start():
    try:
        # Fetch distinct branches from the database
        result_branches = frappe.db.sql("""
            SELECT DISTINCT branch
            FROM `tabUser`
            WHERE role_profile_name = 'Share User Employee'
        """, as_dict=True)

        if result_branches:
            print("\nCreating Day End Documents:")

            # Loop through each branch and create a Day Management Checkin document
            for branch in result_branches:
                # create a new document
                doc = frappe.new_doc('Day Management Checkin')
                doc.branch = branch.get('branch')
                doc.status = "Sanctioned"
                doc.log_type = "Start"
                doc.log_time = now()

                try:
                    doc.insert()
                    print(f"Created Day Start Document for Branch {branch.get('branch')}")
                except frappe.DuplicateEntryError:
                    print(f"Day Start for Branch {branch.get('branch')} already exists.")

        else:
            print("\nNo branches found for day Start")

    except Exception as e:
        print(f"Error: {e}")        
         
def update_barcode():
    print("barcode updated")