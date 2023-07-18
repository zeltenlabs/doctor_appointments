import frappe

from twilio.rest import Client
from frappe.utils.password import get_decrypted_password

def get_twillio_client():
    account_sid = frappe.db.get_single_value("Appointment Twillio Settings", "account_sid")
    auth_token = get_decrypted_password("Appointment Twillio Settings", "Appointment Twillio Settings", "auth_token")
    
    if not account_sid or not auth_token:
        frappe.throw("Please set Twillio Account SID and Auth Token in Doctor Appointments Settings")

    return Client(account_sid, auth_token)

def send_test_message(body, from_, to):
    client = get_twillio_client()
    message = client.messages.create(
        body=body,
        from_="+19896237939",
        to="+919697964142"
    )
    try:
        frappe.get_doc({"Appointment SMS Log": {
        "message_sid": message.sid,
        # "status": message.status,
        "body": message.body,
        "from_": message.from_,
        "to": message.to
        }}).insert(ignore_permissions=True)
    except Exception as e:
        frappe.loge_error("Appointment SMS Log creation failed",e)

    print(message.sid)

