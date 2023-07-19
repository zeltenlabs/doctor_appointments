# Copyright (c) 2023, ZeltenLabs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
    def validate(self):
        # validate the contact_number to be a valid 10 digit phone number except the country code,
        # if it does not have a country code, prepend +91
        if not self.contact_number:
            frappe.throw("Please enter a valid contact number")
        if len(self.contact_number) == 10:
            self.contact_number = f"+91{self.contact_number}"
        elif len(self.contact_number) == 13 and self.contact_number.startswith("+91"):
            pass
        else:
            frappe.throw("Please enter a valid contact number")

    def after_insert(self):
        # add the appointment to the session as a new session item
        self.queue_number = self.add_to_session()
        # attach csrf token + queue number as key and quque number as value
        frappe.cache().set_value(
            f"{frappe.session.id}:queue_number", self.queue_number)
        self.save(ignore_permissions=True)
        self.send_confirmation_message()

    def add_to_session(self):
        filters = {
            "date": self.date,
            "shift": self.shift,
            "clinic": self.clinic
        }
        session_exists = frappe.db.exists("Session", filters)
        if session_exists:
            session = frappe.get_doc("Session", session_exists)
        else:
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
            from_=frappe.db.get_single_value(
                "Appointment Twillio Settings", "from_phone_number"),
            to=self.contact_number
        )
