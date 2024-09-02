import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_share_application_data(filters)

    if not data:
        frappe.msgprint("No Records Found")
        return columns, data

    return columns, data

def get_columns():
    return [
        {
            "fieldname": "saving_current_gl_code",
            "label": "Saving Current GL Code",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "application_sr_no",
            "label": "Application SR No",
            "fieldtype": "Link",
            "options": "Share Application",
            "width": 150,
        },
        {
            "fieldname": "customer_name",
            "label": "Customer Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "ac_open_dt",
            "label": "Account Opening Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "customer_id",
            "label": "Customer ID",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "saving_current_ac_no",
            "label": "Saving Current Account No",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "share_ac_no",
            "label": "Share Account No",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "sanction_date",
            "label": "Sanction Date",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "creator_user_id",
            "label": "Creator User ID",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "creator_name",
            "label": "Creator Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "accepter_user_id",
            "label": "Accepter User ID",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "accepter_name",
            "label": "Accepter Name",
            "fieldtype": "Data",
            "width": 150,
        },
    ]

def get_share_application_data(filters):
    date_conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        date_conditions = f" AND ac_open_dt BETWEEN '{filters['from_date']}' AND '{filters['to_date']}'"

    sql_query = f"""
        SELECT
            saving_current_gl_code,
            branch,
            application_sr_no,
            customer_name,
            ac_open_dt,
            customer_id,
            saving_current_ac_no,
            status,
            share_ac_no,
            CONCAT(
                RIGHT(CONCAT('0', DAY(sanction_date)), 2), '-',
                RIGHT(CONCAT('0', MONTH(sanction_date)), 2), '-',
                YEAR(sanction_date)
            ) AS sanction_date,
            creator_user_id,
            creator_name,
            accepter_user_id,
            accepter_name
        FROM
            `tabShare Application`
        WHERE
            status = 'Sanctioned'
            {date_conditions}
        ORDER BY
            application_sr_no DESC
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return data
