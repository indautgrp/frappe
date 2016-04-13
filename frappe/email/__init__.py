# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.email.email_body import get_email
from frappe.email.smtp import send

def set_customer_supplier(sender,recipients):
	origin_contact = frappe.db.sql("select email_id,supplier,customer,user from `tabContact`",as_dict=1)

	for comm in origin_contact:
		if comm["user"] is None and comm["email_id"]:
			if (sender and sender.find(comm["email_id"]) > -1) or (
				recipients and recipients.find(comm["email_id"]) > -1):
				if comm["supplier"] and comm["customer"]:
					return {"supplier": comm["supplier"], "customer": comm["customer"]}

				elif comm["supplier"]:
					return {"supplier": comm["supplier"], "customer": None}

				elif comm["customer"]:
					return {"supplier": None, "customer": comm["customer"]}
	return {"supplier": None, "customer": None}

def sendmail_md(recipients, sender=None, msg=None, subject=None, attachments=None, content=None,
	reply_to=None, cc=(), message_id=None):
	"""send markdown email"""
	import markdown2
	sendmail(recipients, sender, markdown2.markdown(content or msg), subject, attachments, reply_to=reply_to, cc=cc)

def sendmail(recipients, sender='', msg='', subject='[No Subject]', attachments=None, content=None,
	reply_to=None, cc=(), message_id=None):
	"""send an html email as multipart with attachments and all"""
	mail = get_email(recipients, sender, content or msg, subject, attachments=attachments, reply_to=reply_to, cc=cc)
	if message_id:
		mail.set_message_id(message_id)

	send(mail)

def sendmail_to_system_managers(subject, content):
	send(get_email(get_system_managers(), None, content, subject))

@frappe.whitelist()
def get_contact_list():
	"""Returns contacts (from autosuggest)"""
	cond = ['`%s` like "%s%%"' % (frappe.db.escape(f),
		frappe.db.escape(frappe.form_dict.get('txt'))) for f in frappe.form_dict.get('where').split(',')]
	cl = frappe.db.sql("select `%s` from `tab%s` where %s" % (
  			 frappe.db.escape(frappe.form_dict.get('select'))
			,frappe.db.escape(frappe.form_dict.get('from'))
			,' OR '.join(cond)
		)
	)
	frappe.response['cl'] = filter(None, [c[0] for c in cl])

def get_system_managers():
	return frappe.db.sql_list("""select parent FROM tabUserRole
		WHERE role='System Manager'
		AND parent!='Administrator'
		AND parent IN (SELECT email FROM tabUser WHERE enabled=1)""")
