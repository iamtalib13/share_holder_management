import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    data, columns = [], []

    columns = get_columns()
    share_application_data = get_share_application_data(filters)

    if not share_application_data:
        frappe.msgprint("No Records Found")
        return columns, data

    for d in share_application_data:
        row = {
            "application_sr_no": d.application_sr_no,
            "customer_id": d.customer_id,
            "share_ac_no": d.share_ac_no,
            "customer_name": d.customer_name,
            "branch": d.branch,
            "gender": d.gender,
            "aadhaar_number": d.aadhaar_number,
            "sanction_date": d.sanction_date,
            "no_of_shares": d.no_of_shares,
            "base_share_amount": d.base_share_amount,
            "share_application_charges": d.share_application_charges,
            "Total_Amount": d.Total_Amount
        }
        data.append(row)

    return columns, data

def get_columns():
    return [
        {
            "fieldname": "application_sr_no",
            "label": "Application SR No",
            "fieldtype": "Link",
            "options": "Share Application",
            "width": "150",
        },
        {
            "fieldname": "customer_id",
            "label": "Customer ID",
            "fieldtype": "Data",
            "width": "100",
        },
        {
            "fieldname": "share_ac_no",
            "label": "Share Account No",
            "fieldtype": "Data",
            "width": "150",
        },
        {
            "fieldname": "customer_name",
            "label": "Customer Name",
            "fieldtype": "Data",
            "width": "150",
        },
        {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Data",
            "width": "100",
        },
        {
            "fieldname": "gender",
            "label": "Gender",
            "fieldtype": "Data",
            "width": "100",
        },
        {
            "fieldname": "aadhaar_number",
            "label": "Aadhaar Number",
            "fieldtype": "Data",
            "width": "150",
        },
        {
            "fieldname": "sanction_date",
            "label": "Sanction Date",
            "fieldtype": "Data",
            "width": "100",
        },
        {
            "fieldname": "no_of_shares",
            "label": "Number of Shares",
            "fieldtype": "Data",
            "width": "100",
        },
        {
            "fieldname": "base_share_amount",
            "label": "Base Share Amount",
            "fieldtype": "Currency",
            "width": "120",
        },
        {
            "fieldname": "share_application_charges",
            "label": "Share Application Charges",
            "fieldtype": "Currency",
            "width": "160",
        },
        {
            "fieldname": "Total_Amount",
            "label": "Total Amount",
            "fieldtype": "Currency",
            "width": "120",
        }
    ]

def get_share_application_data(filters):
    # Build the SQL query to fetch data from the "Share Application" doctype
    sql_query = """
        SELECT
            application_sr_no,
            customer_id,
            share_ac_no,
            customer_name,
            branch,
            gender,
            aadhaar_number,
            CONCAT(
               RIGHT(CONCAT('0', DAY(sanction_date)), 2), '-',
               RIGHT(CONCAT('0', MONTH(sanction_date)), 2), '-',
               YEAR(sanction_date)
            ) AS sanction_date,
            no_of_shares,
            base_share_amount,
            share_application_charges,
            tot_share_amt AS Total_Amount
        FROM
            `tabShare Application`
        WHERE
            status='Sanctioned'
    """

    # Apply branch filter if provided
    if filters.get("branch"):
        sql_query += f" AND branch = '{filters['branch']}'"

    # Execute the SQL query
    data = frappe.db.sql(sql_query, as_dict=True)

    return data

