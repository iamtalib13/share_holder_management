import frappe

@frappe.whitelist()
def netwin():
    user = frappe.session.user
    # Fetch the branch_code from the User DocType
    branch_code = frappe.db.get_value("User", user, "branch_code")
    # Return branch_code if found, else return "All"
    return branch_code if branch_code else "All"
