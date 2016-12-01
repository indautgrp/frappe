from __future__ import unicode_literals
import frappe


def execute():
	for data in frappe.db.sql("""SELECT GROUP_CONCAT(name order by creation) as names,  COUNT(unique_id) c FROM tabCommunication 
		where unique_id is not null GROUP BY email_account, unique_id HAVING c > 1""", as_dict=1):

		for d in data.names.split(",")[1:]:
			frappe.db.sql("delete from tabCommunication where name = %s ", (d))