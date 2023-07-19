# Copyright (c) 2023, ZeltenLabs and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Clinic(WebsiteGenerator):
	def on_update(self):
		# if field doctor_in is changed publish a realtime event called doctor_status_changed
		if self.has_value_changed("doctor_in"):
			print("doctor_in changed")
			frappe.publish_realtime('doctor_status_changed', {"doctor_in": self.doctor_in, "clinic": self.name})
