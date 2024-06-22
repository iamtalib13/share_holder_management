import frappe
from frappe import _
from frappe.model.document import Document
import re
from datetime import datetime


class ShareApplication(frappe.model.document.Document):
    pass

    def before_validate(self):
        self._validate_aadhaar_number()
        self._validate_mobile_number()
        self._validate_pan_number()
        self._validate_no_of_shares()

    def _validate_aadhaar_number(self):
        if self.aadhaar_number and len(str(self.aadhaar_number)) != 12:
            frappe.throw(
                _("Aadhar number is not valid, It must be 12 digits."),
                title=_("Please provide the proper Aadhar number."),
            )

    def _validate_mobile_number(self):
        if self.mobile and len(str(self.mobile)) != 10:
            frappe.throw(
                _("Mobile number is not valid, it must be 10 digits."),
                title=_("Please provide the proper mobile number."),
            )

    def _validate_pan_number(self):
        if self.pan_no:
            pan_pattern = re.compile(r"^[A-Z]{5}\d{4}[A-Z]{1}$")
            if not pan_pattern.match(str(self.pan_no)):
                frappe.throw(
                    _(
                        "PAN Number is not valid. It should be in the format: ABCDE1234F"
                    ),
                    title=_("Please provide a valid PAN number."),
                )

    def _validate_no_of_shares(self):
        if not self.no_of_shares or self.no_of_shares == 0:
            frappe.throw(
                _("Please provide the proper no. of shares."),
                title=_("Invalid number of shares."),
            )



    def before_save(self):
        self.application_sr_no = self.name
        self._calculate_share_amount()

        if self.status == "Sanctioned":
            if not self.share_ac_no:
                self._set_share_ac_no()

    def _create_share_ac_no(self):
        try:
            # Create a new Share Account Number
            doc = frappe.new_doc("Share Account")
            doc.share_application_number = self.name
            doc.insert(ignore_permissions=True)  # Ignore permissions to allow creation
        except Exception as e:
            frappe.log_error(f"Error creating Share Account: {e}")

    def _set_share_ac_no(self):
        try:
            # Find and Set a Share Account Number
            share_account_number = frappe.db.get_value(
                "Share Account", {"share_application_number": self.name}, "name"
            )
            if share_account_number:
                self.share_ac_no = share_account_number
            else:
                self._create_share_ac_no()  # Create if not found
            share_account_number = frappe.db.get_value(
                "Share Account", {"share_application_number": self.name}, "name"
            )
            
            if share_account_number:
                self.share_ac_no = share_account_number
            else:
                frappe.log_error(
                    f"Unable to set Share Account Number for Share Application {self.name}"
                )
        except Exception as e:
            frappe.log_error(f"Error setting Share Account Number: {e}")

    def _calculate_share_amount(self):
        self.base_share_amount = self.no_of_shares * 10
        self.tot_share_amt = self.base_share_amount + 10
        self.share_customer_name = self.customer_name
        self.acc_name = self.customer_name



@frappe.whitelist()
def check_last_share_ac_no():
    result = frappe.db.sql(
        """SELECT share_ac_no FROM `tabShare Application`
                             ORDER BY CAST(share_ac_no AS SIGNED) DESC LIMIT 1""",
        as_dict=True,
    )

    if result:
        last_share_ac_no = result[0]["share_ac_no"]
        return int(last_share_ac_no) + 1
    else:
        frappe.msgprint("No records found in the 'Share Account Number' table.")


@frappe.whitelist()
def check_branch_and_branch_code(owner):
    result = frappe.db.sql(
        f"""SELECT branch, branch_code, user_id
                               FROM `tabEmployee`
                               WHERE user_id='{owner}';""",
        as_dict=True,
    )

    if result:
        return result[0]
    else:
        frappe.msgprint(
            f"No records found for user_id '{owner}' in the 'Employee' table."
        )
        return None


@frappe.whitelist()
def check_current_enable_share_amount():
    result = frappe.db.sql(
        f"""SELECT amount FROM `tabShare Amount Details`
                               WHERE status='Enable'
                               LIMIT 1;""",
        as_dict=True,
    )

    if result:
        return result[0]["amount"]
    else:
        frappe.msgprint("Server Error - Current share amount not detected")
        return None


@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()


@frappe.whitelist()
def get_existing_customer(customer_id):
    check_exist_customer = frappe.db.sql(
        f"""
        SELECT 
            CASE 
                WHEN EXISTS (SELECT 1 FROM `tabShare Application` WHERE customer_id = '{customer_id}') THEN 1
                ELSE 0
            END AS exist;
    """
    )

    if check_exist_customer:
        if check_exist_customer[0][0]:  # If True
            return "True"

        else:
            return "False"
    else:
        return "False"  # Or whatever default value you prefer


@frappe.whitelist()
def share_certificate_template(docname):
    doc = frappe.get_doc("Share Application", docname)
    html_content = frappe.render_template(
        "share_holder_management/share_holder_management/doctype/share_application/templates/share_certificate_template.html",
        {"doc": doc},
    )
    return {"html_content": html_content}


@frappe.whitelist()
def get_branch_checkin_details(branch, date):
    # today_datetime = frappe.utils.now_datetime()

    check_ho_day_start = frappe.db.sql(
        f"""SELECT log_type FROM `tabDay Management Checkin`
                                           WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'Start'
                                           LIMIT 1""",
        (date, "Gondia HO"),
        as_dict=True,
    )

    check_branch_day_start = frappe.db.sql(
        f"""SELECT log_type FROM `tabDay Management Checkin`
                                               WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'Start'
                                               LIMIT 1""",
        (date, branch),
        as_dict=True,
    )

    check_branch_day_end = frappe.db.sql(
        f"""SELECT log_type FROM `tabDay Management Checkin`
                                             WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'End'
                                             LIMIT 1""",
        (date, branch),
        as_dict=True,
    )

    html_table = "<table border='1'>"
    html_table += "<tr><th>Log Type</th></tr>"

    if check_ho_day_start:
        html_table += f"<tr><td>{check_ho_day_start[0].get('log_type')}</td></tr>"

    if check_branch_day_start:
        html_table += f"<tr><td>{check_branch_day_start[0].get('log_type')}</td></tr>"

    html_table += "</table>"

    if check_ho_day_start and check_branch_day_start:
        flag = "Day Start"
        if check_branch_day_end:
            flag = "Branch Day Ended"
    elif check_ho_day_start:
        flag = "Branch Day Not Started"
    else:
        flag = "Branch and HO Day Not Started"

    return flag
