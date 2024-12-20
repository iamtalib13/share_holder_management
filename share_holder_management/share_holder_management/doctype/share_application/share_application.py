import frappe
from frappe import _
from frappe.model.document import Document
import re
from datetime import datetime
class ShareApplication(Document):

    def before_insert(self):
        self.no_of_shares = 1
    #    user_id = frappe.session.user.split('@')[0]
    #    fname, lname = frappe.db.get_value('Employee', {'employee_id': user_id}, ['first_name', 'last_name'])
    #    self.creator_user_id = user_id
    #    self.creator_name = f"{fname} {lname}"
    def on_change(self):
        if self.status == "Submitted":
           frappe.enqueue_doc(
                                self.doctype,  # The doctype of the document
                                self.name,     # The name (ID) of the document
                                "create_account",   # The method to be called
                                queue="short", # Use the "short" queue
                                timeout=500    # Timeout in seconds
                            )
           
        if self.status == "Sanctioned":
            self.create_journal_entry()
        #    frappe.enqueue_doc(
        #                         self.doctype,  # The doctype of the document
        #                         self.name,     # The name (ID) of the document
        #                         "create_journal_entry",   # The method to be called
        #                         queue="short", # Use the "short" queue
        #                         timeout=500    # Timeout in seconds
        #                     )       
    
    def create_account(self):
        # Prepare the account details
        account_details = {
            'doctype': 'Account',
            'account_name': self.customer_name,  # Use customer_name for the account name
            'account_type': 'Bank',         # Set account type to Receivable
            'is_group': 0,                        # Set is_group to 0 for a regular account
            'parent_account': "Bank Accounts - Sahayog",  # Set parent account
            'account_number': self.saving_current_ac_no,  # Use the provided account number
            # Add any additional fields as necessary
        }

        # Create and insert the account document
        account = frappe.get_doc(account_details)
        
        try:
            account.insert(ignore_permissions=True)
            frappe.msgprint(f"Account '{account.account_name}' created successfully.")
        except Exception as e:
            frappe.msgprint(f"Failed to create account: {str(e)}")
        
    def create_journal_entry(self):
        try:
            # Check if a Journal Entry already exists for this `self.name`
            existing_entry = frappe.db.exists(
                "Journal Entry", {"custom_share_application_id": self.name}
            )
            if existing_entry:
                frappe.msgprint(
                    f"A Journal Entry already exists for this Share Application ({self.name}): {existing_entry}",
                    indicator="yellow",
                    alert=True,
                )
                return  # Stop further execution if an entry exists

            # Validate the existence of `self.saving_current_ac_no`
            if not self.saving_current_ac_no:
                frappe.throw("Saving/Current Account Number is required to create a Journal Entry.")

            # Fetch the linked account using the custom account number
            main_account = frappe.db.get_value("Account", {"account_number": self.saving_current_ac_no}, "name")
            if not main_account:
                frappe.throw(f"No account found with custom account number: {self.saving_current_ac_no}")

            # Prepare the child table data with the custom account number
            accounts = [
                {
                    "account": main_account,
                    "party_type": None,
                    "party": None,
                    "debit_in_account_currency": 20.00,
                    "credit_in_account_currency": 0.00,
                },
                {
                    "account": "100001410010001 - SH -  SHARE ACCOUNT - Sahayog",
                    "party_type": None,
                    "party": None,
                    "debit_in_account_currency": 0.00,
                    "credit_in_account_currency": 10.00,
                },
                {
                    "account": "100001670060001 - MBEFEE - SHARE MEMBER ENTRY FEE - Sahayog",
                    "party_type": None,
                    "party": None,
                    "debit_in_account_currency": 0.00,
                    "credit_in_account_currency": 10.00,
                },
            ]

            # Create the Journal Entry in draft mode
            journal_entry = frappe.get_doc({
                "doctype": "Journal Entry",
                "posting_date": frappe.utils.today(),
                "voucher_type": "Journal Entry",
                "custom_share_application_id": self.name,
                "accounts": accounts,
                "docstatus": 0,
            })

            # Insert the Journal Entry
            journal_entry.insert()
            frappe.msgprint(f"Journal Entry {journal_entry.name} created successfully.")

        except Exception as e:
            # Log the error for debugging
            frappe.log_error(message=str(e), title="Journal Entry Creation Failed")

            # Notify the user with an error message
            frappe.msgprint(
                f"An error occurred while creating the Journal Entry: {str(e)}",
                indicator="red",
                alert=True,
            )

      

    def before_save(self):
        # Convert customer name to uppercase and assign to relevant fields
        upper_case_name = self.customer_name.upper()
        self.customer_name = upper_case_name
        self.share_customer_name = upper_case_name
        self.acc_name = upper_case_name    

        self.application_sr_no = self.name
        self._calculate_share_amount()

        if self.status == "Sanctioned" and not self.share_ac_no:
            self._set_share_ac_no()
            user_id = frappe.session.user.split('@')[0]
            fname, lname = frappe.db.get_value('Employee', {'employee_id': user_id}, ['first_name', 'last_name'])
            self.accepter_user_id = user_id
            self.accepter_name = f"{fname} {lname}"
            self.status = "Sanctioned"

    def _set_share_ac_no(self):
        try:
            # Retrieve or create the Share Account Number
            share_account_number = frappe.db.get_value("Share Account", {"share_application_number": self.name}, "name")
            if not share_account_number:
                share_account_number = self._create_share_ac_no()
            
            if share_account_number:
                self.share_ac_no = share_account_number
            else:
                frappe.throw("Failed to create or retrieve Share Account Number. Please try again.")
        except Exception as e:
            frappe.throw(f"Error setting Share Account Number: {str(e)}")

    def _create_share_ac_no(self):
        # Create a new Share Account and return its name
        doc = frappe.new_doc("Share Account")
        doc.share_application_number = self.name
        doc.customer_id = self.customer_id
        doc.insert(ignore_permissions=True)
        return doc.name if doc.name else None


       
    def validate(self):
        pass
        #self._validate_aadhaar_number()
        #self._validate_mobile_number()
        #self._validate_pan_number()
        #self._validate_no_of_shares()

    def _validate_aadhaar_number(self):
        # Check if status is not "Sanctioned"
        if self.status != "Sanctioned":
            # Validate Aadhaar number
            if self.aadhaar_number and len(str(self.aadhaar_number)) != 12:
                frappe.throw(
                    _("Aadhaar number is not valid, It must be 12 digits."),
                    title=_("Please provide the proper Aadhaar number."),
                )

    def _validate_mobile_number(self):
        pass
        # Check if status is not "Sanctioned"
        # if self.status != "Sanctioned":
        #     # Validate mobile number
        #     if self.mobile and len(str(self.mobile)) != 10:
        #         frappe.throw(
        #             _("Mobile number is not valid, it must be 10 digits."),
        #             title=_("Please provide the proper mobile number."),
        #         )

    def _validate_pan_number(self):
        # Check if status is not "Sanctioned"
        if self.status != "Sanctioned":
            # Validate PAN number
            if self.pan_no:
                pan_pattern = re.compile(r"^[A-Z]{5}\d{4}[A-Z]{1}$")
                if not pan_pattern.match(str(self.pan_no)):
                    frappe.throw(
                        _("PAN Number is not valid. It should be in the format: ABCDE1234F"),
                        title=_("Please provide a valid PAN number."),
                    )

    def _validate_no_of_shares(self):
        if not self.no_of_shares or self.no_of_shares == 0:
            frappe.throw(
                _("Please provide the proper number of shares."),
                title=_("Invalid number of shares."),
            )

   
    def _calculate_share_amount(self):
        self.base_share_amount = self.no_of_shares * 10
        self.tot_share_amt = self.base_share_amount + 10

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
        return "False"

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
