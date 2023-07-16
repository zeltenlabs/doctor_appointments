# Copyright (c) 2023, ZeltenLabs and Contributors
# See license.txt

import frappe
from frappe.utils import today
from frappe.tests.utils import FrappeTestCase
from doctor_appointments.doctor_appointments.doctype.session.session import create_sessions

class TestSession(FrappeTestCase):
	def test_create_sessions(self):
		doctor = frappe.get_doc({"doctype": "Doctor", "first_name": "Test Doctor", "speciality": "Gastro"}).insert()
		clinic = frappe.get_doc({"doctype": "Clinic", "name": "Test Clinic", "doctor": doctor.name, "contact_number": "999", "is_published": True}).insert()
		shift1 = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "9:00:00","end_time": "15:00:00", "clinic": clinic.name}).insert()
		shift2 = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "15:00:00","end_time": "21:00:00", "clinic": clinic.name}).insert()
		# asert that there are no sessions
		self.assertEqual(frappe.db.count("Session"), 0)

		# create sessions
		create_sessions()

		# assert that there is one session
		self.assertEqual(frappe.db.count("Session"), 2)

		# and that session is for the above clinic and today's shift
		session = frappe.get_doc("Session", {"clinic": clinic.name, "shift": shift1.name, "date": today()})
		self.assertTrue(session)

	def tearDown(self):
		frappe.db.rollback()