# Copyright (c) 2023, ZeltenLabs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today
from frappe.model.document import Document


class Session(Document):
	pass

def create_sessions():
	if frappe.flags.in_test:
		clinics = frappe.get_all("Clinic", filters={"is_published": True, "name": "Test Clinic"}, pluck="name")
	else:
		clinics = frappe.get_all("Clinic", filters={"is_published": True}, pluck="name")
	
	for clinic in clinics:
		# create a session if it does not exist, use if_duplicate=True
		# to ignore duplicate entry error
		shifts = frappe.get_all("Schedule Shift", filters={"clinic": clinic}, pluck="name")
		for shift in shifts:
			frappe.get_doc({
				"doctype": "Session",
				"clinic": clinic,
				"shift": shift,
				"date": today()
			}).insert(ignore_permissions=True, ignore_if_duplicate=True)
		