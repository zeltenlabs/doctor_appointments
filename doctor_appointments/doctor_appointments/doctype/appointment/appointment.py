# Copyright (c) 2023, ZeltenLabs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
	def after_insert(self):
		# add the appointment to the session as a new session item
		print("your queue number:",self.add_to_session())
	def add_to_session(self):
		session = frappe.get_doc("Session", {"date": self.date, "shift": self.shift, "clinic": self.clinic})

		session.append("queue", {
			"appointment": self.name,
			"status": "Pending"
		})
		session.save(ignore_permissions=True)

		return len(session.queue)
