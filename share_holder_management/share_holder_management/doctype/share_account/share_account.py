# Copyright (c) 2024, Talib Sheikh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ShareAccount(Document):
	pass
	def before_save(self):
		self.share_account_number = self.name
	
	def before_insert(self):
		self.share_account_number = self.name
