# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class CommunicationReconciliation(Document):
	def fetch(self):
		dt = self.reference_doctype
		dn = self.reference_name
		conditions = "<=>"
		if (dn =="" or dn== None):
			if (dt =="" or dt== None):
				dt = dn = None
			else:
				conditions = "like"
				dn = "%"

		select= """select name, content , sender , creation, recipients, communication_medium as comment_type, subject, status ,reference_doctype,reference_name
					from tabCommunication
					where reference_doctype <=> %s and reference_name {0} %s
					order by creation desc""".format(conditions)

		self.communication_list = []
		communications = frappe.db.sql(select,(dt,dn),as_dict=1)
		for c in communications:
			comm = self.append('communication_list', {})

			comm.name = c.get('name')
			comm.reference_doctype = c.get('reference_doctype')
			comm.reference_name = c.get('reference_name')
			if c.get('recipients') != None:
				comm.recipients = c.get('recipients').replace('"',"").strip("<>")
			comm.sender = c.get('sender')
			comm.subject = c.get('subject')
			comm.status = c.get('status')
			comm.content = c.get('content')
			
		return self

	def relink_bulk(self,changed_list):
		for comm in changed_list:
			frappe.db.sql("""update `tabCommunication`
			set reference_doctype = %s ,reference_name = %s ,status = "Linked"
			where name = %s """,(changed_list[comm]["reference_doctype"],changed_list[comm]["reference_name"],changed_list[comm]["name"]))
		return self.fetch()

@frappe.whitelist()
def relink(name,reference_doctype,reference_name):
		dt = reference_doctype
		dn = reference_name
		if dt=="" or dt==None or dn == "" or dn == None:
			return 
		frappe.db.sql("""update `tabCommunication`
			set reference_doctype = %s ,reference_name = %s ,status = "Linked"
			where name = %s """,(dt,dn,name))

def get_communication_doctype(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond
	return frappe.db.sql("""select name,module
		from `tabDocType`
		WHERE issingle = 0
		and istable = 0
		and hide_toolbar = 0
		and ({key} like %(txt)s)
		{mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			name
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})
