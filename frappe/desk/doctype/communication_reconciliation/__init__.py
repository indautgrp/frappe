import frappe
@frappe.whitelist(allow_guest=True)
def relink(self,name,reference_doctype,reference_name):
	#pydevd.settrace('192.168.8.113', port=132, stdoutToServer=True, stderrToServer=True)

	dt = reference_doctype
	dn = reference_name
	#dt = ""#self.reference_doctype
	#dn = ""#self.reference_name
	#for comm in self.communication_list:
	#	if comm.new_reference_doctype!=None and comm.new_reference_name!=None:
	#		dt = comm.new_reference_doctype
	#		dn = comm.new_reference_name
	#		name = comm.name
	#	#probably need a catch to check if more that one is found


	if dt=="" or dt==None or dn == "" or dn == None:
		return # is blank maybe try flash missing required
	#frappe.db.sql("""update `tabCommunication`
	#	set reference_doctype = %s ,reference_name = %s ,status = "Linked"
	#	where name = %s """,(dt,dn,name))


	frappe.db.set_value("Communication",name,"reference_doctype",dt)
	frappe.db.set_value("Communication",name,"reference_name",dn)
	frappe.db.set_value("Communication",name,"status","Linked")

	return self.fetch()