import frappe
from frappe import _
from frappe.model.document import Document
import re

class ShareApplication(Document):
    def before_validate(self):
        self._validate_status_and_nominee()
        self._validate_aadhaar_number()
        self._validate_pan_number()
        self._validate_no_of_shares()

    def _validate_status_and_nominee(self):
        if self.status == "Submitted" and not self.nominee_details:
            frappe.throw("Please Add atleast one Nominee before submit the form")

    def _validate_aadhaar_number(self):
        if self.aadhaar_number:
            if len(str(self.aadhaar_number)) != 12:
              frappe.throw(_("Aadhar number is not valid, It must be 12 digits."), title=_("Please provide the proper Aadhar number."))

    def _validate_pan_number(self):
        if self.pan_no:
            pan_pattern = re.compile(r"^[A-Z]{5}\d{4}[A-Z]{1}$")
            if not pan_pattern.match(str(self.pan_no)):
                frappe.throw(_("PAN Number is not valid. It should be in the format: ABCDE1234F"), title=_("Please provide a valid PAN number."))

    def _validate_no_of_shares(self):
        if self.no_of_shares is None or self.no_of_shares == 0:
            frappe.throw(_("Please provide the proper no. of shares."), title=_("Invalid number of shares."))

    def before_insert(self):
        self._set_application_sr_no()

    def _set_application_sr_no(self):
        self.application_sr_no = self._get_last_application_sr_no() + 1

    def _get_last_application_sr_no(self):
        last_sr_no = frappe.db.sql("""SELECT application_sr_no FROM `tabShare Application`
                                      ORDER BY CAST(application_sr_no AS SIGNED) DESC LIMIT 1""")
        return last_sr_no[0][0] if last_sr_no else 0

    def before_save(self):
        self._calculate_share_amount()
        
    def _calculate_share_amount(self):
     if self.status == "Draft":
        self.base_share_amount = self.no_of_shares * 10
        self.tot_share_amt = self.base_share_amount + 10
        self.share_customer_name = self.customer_name
        self.acc_name = self.customer_name
        self.share_ac_no = self._get_last_share_ac_no() + 1


    def _get_last_share_ac_no(self):
        last_ac_no = frappe.db.sql("""SELECT share_ac_no FROM `tabShare Application`
                                      ORDER BY CAST(share_ac_no AS SIGNED) DESC LIMIT 1""")
        return last_ac_no[0][0] if last_ac_no else 0

@frappe.whitelist()
def check_last_application_sr_no():
    result = frappe.db.sql("""SELECT application_sr_no FROM `tabShare Application`
                             ORDER BY CAST(application_sr_no AS SIGNED) DESC LIMIT 1""",
                           as_dict=True)

    if result:
        last_application_sr_no = result[0]['application_sr_no']
        return last_application_sr_no + 1
    else:
        frappe.msgprint("No records found in the 'Share Application' table.")

@frappe.whitelist()
def check_last_share_ac_no():
    result = frappe.db.sql("""SELECT share_ac_no FROM `tabShare Application`
                             ORDER BY CAST(share_ac_no AS SIGNED) DESC LIMIT 1""",
                           as_dict=True)

    if result:
        last_share_ac_no = result[0]['share_ac_no']
        return int(last_share_ac_no) + 1
    else:
        frappe.msgprint("No records found in the 'Share Account Number' table.")

@frappe.whitelist()
def check_branch_and_branch_code(owner):
    result = frappe.db.sql(f"""SELECT branch, branch_code, user_id
                               FROM `tabEmployee`
                               WHERE user_id='{owner}';""",
                           as_dict=True)

    if result:
        employee_data = result[0]
        return employee_data
    else:
        frappe.msgprint(f"No records found for user_id '{owner}' in the 'Employee' table.")
        return None

@frappe.whitelist()
def check_current_enable_share_amount():
    result = frappe.db.sql(f"""SELECT amount FROM `tabShare Amount Details`
                               WHERE status='Enable'
                               LIMIT 1;""",
                           as_dict=True)

    if result:
        current_share_amount = result[0]['amount']
        return current_share_amount
    else:
        frappe.msgprint("Server Error - Current share amount not detected")
        return None

@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()

@frappe.whitelist()
def share_certificate_template(docname):
    doc = frappe.get_doc("Share Application", docname)
    html_content = frappe.render_template("share_holder_management/share_holder_management/doctype/share_application/templates/share_certificate_template.html", {"doc": doc})
    return {"html_content": html_content}

@frappe.whitelist()
def get_branch_checkin_details(branch):
    today_datetime = frappe.utils.now_datetime()

    check_ho_day_start = frappe.db.sql(f"""SELECT log_type FROM `tabDay Management Checkin`
                                           WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'Start'
                                           LIMIT 1""",
                                       (today_datetime.date(), "Gondia HO"),
                                       as_dict=True)

    check_branch_day_start = frappe.db.sql(f"""SELECT log_type FROM `tabDay Management Checkin`
                                               WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'Start'
                                               LIMIT 1""",
                                           (today_datetime.date(), branch),
                                           as_dict=True)

    check_branch_day_end = frappe.db.sql(f"""SELECT log_type FROM `tabDay Management Checkin`
                                             WHERE DATE(log_time) = %s AND branch = %s AND log_type = 'End'
                                             LIMIT 1""",
                                         (today_datetime.date(), branch),
                                         as_dict=True)

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
