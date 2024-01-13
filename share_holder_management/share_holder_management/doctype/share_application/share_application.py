# Copyright (c) 2023, Talib Sheikh and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document

class ShareApplication(Document):
    pass

#     def before_save(self):
#         # Check if no_of_shares is null
#         if self.no_of_shares is None:
#             frappe.throw(
#                 _("It should not be blank"),
#                 title=_("Please provide the proper no. of shares."),
               
#             )

#         # # Check if no_of_shares is zero
#         # elif self.no_of_shares == 0:
#         #     frappe.throw(
#         #         _("Zero is not a correct share"),
#         #         title=_("Please provide the proper no. of shares.")
#         #     )
    
#     def before_validate(self):
#          if self.no_of_shares == 0:
#              frappe.throw("No. of Share cannot be 0")
             


#     def before_insert(self):
#         self.base_share_amount = self.no_of_shares * 100  
           
#         self.tot_share_amt = (self.no_of_shares * 100) + 10
#         self.share_customer_name = self.customer_name
#         self.acc_name = self.customer_name
#         self.saving_current_ac_no = self.ac_no
        
        
# @frappe.whitelist()
# def check_last_application_sr_no():
#     result = frappe.db.sql(
#         """SELECT application_sr_no
#            FROM `tabShare Application`
#            ORDER BY CAST(application_sr_no AS SIGNED) DESC
#            LIMIT 1;""",
#         as_dict=True,
#     )

#     if result:
#         last_application_sr_no = result[0]['application_sr_no']
#         frappe.msgprint(f"Last Application Sr. No.: {last_application_sr_no}")
#         return last_application_sr_no + 1
#     else:
#         frappe.msgprint("No records found in the 'Share Application' table.")

@frappe.whitelist()
def get_server_datetime():
    return frappe.utils.now_datetime()