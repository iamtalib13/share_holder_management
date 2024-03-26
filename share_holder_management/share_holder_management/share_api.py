import frappe


@frappe.whitelist()
def get_share_data():
    return frappe.db.sql(
        f"""select department,division,region,user_id,branch from `tabEmployee`;""",
        as_dict=True,
    )