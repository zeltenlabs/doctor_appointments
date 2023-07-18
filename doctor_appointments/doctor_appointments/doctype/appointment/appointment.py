# Copyright (c) 2023, ZeltenLabs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
	def after_insert(self):
		# add the appointment to the session as a new session item
		self.queue_number = self.add_to_session()
		# attach csrf token + queue number as key and quque number as value
		frappe.cache().set_value(f"{frappe.session.id}:queue_number", self.queue_number)
		self.save(ignore_permissions=True)
		self.send_confirmation_message()

	def add_to_session(self):
		filters= {"date": self.date, "shift": self.shift, "clinic": self.clinic}
		session_exists = frappe.db.exists("Session", filters)
		if session_exists:
			session = frappe.get_doc("Session", session_exists)
		else :
			session = frappe.new_doc("Session")
			session.update(filters)
			session.save(ignore_permissions=True)

		session.append("queue", {
			"appointment": self.name,
			"status": "Pending"
		})
		session.save(ignore_permissions=True)

		return len(session.queue)

	def send_confirmation_message(self):
		frappe.enqueue(
			"doctor_appointments.utils.send_test_message",
			body=f"Your appointment is confirmed for {self.date} at {self.shift} in {self.clinic} \n Your queue number is {self.queue_number}",
			from_="+19896237939",
			to=self.contact_number
		)