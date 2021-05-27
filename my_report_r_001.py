# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _
from frappe.utils import flt,cstr
from erpnext.accounts.report.financial_statements import get_period_list

def execute(filters=None):
    columns, data = [], []
    columns=get_columns()
    print("filters from main method : ",filters)
    data=get_log_data(filters)
    print('data from main method : ',data)
    report_summary = [
        {
        "value": 100,
        "indicator": "Green" ,
        "label": _("Total Profit This Year"),
        "datatype": "Currency",
        "currency": "INR"
    },
      {
                        "value": 20,
                        "label": "Total Asset",
                        "datatype": "Currency",
                        "currency": "INR",
                        "indicator": "Red" ,
                },]

    message='Hai,this is message'
    chart = None

    ext_data = get_salary()
    emp_data = get_emp_list()

    data_to_be_printed={"ext_data":ext_data,"condition_text":'XXXXXXXXX  This is an extra-data for testing XXXXXXXX .n',"emp_data":emp_data}

    return columns, data, message, chart, report_summary,data_to_be_printed




def get_columns():
    columns = [_("License") + ":Link/Vehicle:100", _('Create') + ":data:50",
            _("Model") + ":data:50", _("Location") + ":data:100",
            _("Log") + ":Link/Vehicle Log:100", _("Odometer") + ":Int:80",
            _("Date") + ":Date:100", _("Fuel Qty") + ":Float:80",
            _("Fuel Price") + ":Float:100",_("Fuel Expense") + ":Float:100",
            _("Service Expense") + ":Float:100"
    ]
    return columns
    
    def get_service_expense():

    expense_amount = frappe.db.sql("""select sum(license_plate) as sum
                from `tabVehicle` log""",as_dict=True)

    print("Expense amount is : ",expense_amount)

    # return flt(expense_amount[0][0]) if expense_amount else 0
    return 0

def get_log_data(filters):

    data=None
    l_no = filters.get('lic')
    selected_month = filters.get('month')
    print("license number : ",l_no)
    print("selected month is : ",selected_month)

    if(l_no):
        data = frappe.db.sql("""select
                        vhcl.license_plate as "License", vhcl.make as "Make", vhcl.model as "Model",
                        vhcl.location as "Location", log.name as "Log", log.odometer as "Odometer",
                        log.date as "Date", log.fuel_qty as "Fuel_Qty", log.price as "Fuel_Price",
                        log.fuel_qty * log.price as "Fuel_Expense"
                from
                        `tabVehicle` vhcl,`tabVehicle Log` log where vhcl.license_plate = %s""",(l_no),as_dict=True)
    else:
        data = frappe.db.sql("""select
                        vhcl.license_plate as "License", vhcl.make as "Make", vhcl.model as "Model",
                        vhcl.location as "Location", log.name as "Log", log.odometer as "Odometer",
                        log.date as "Date", log.fuel_qty as "Fuel_Qty", log.price as "Fuel_Price",
                        log.fuel_qty * log.price as "Fuel_Expense"
                from
                        `tabVehicle` vhcl,`tabVehicle Log` log """,as_dict=True)


    dl=list(data)
    record=[]
    expense_amount = get_service_expense()
    for row in dl:
        data_holder=[row.License,row.Make,row.Model,row.Location,row.Log,row.Odometer,row.Date,row.Fuel_Qty,row.Fuel_Price,row.Fuel_Expense,10]
        record.append(data_holder)
    return record

def get_salary():
    emp_local_data=[]
    basic = 1000
    loop_range=20
    for i in range(loop_range):
        name = 'Emp '+str(i)
        month='April'
        salary = basic+i
        dict_value = {
            "name":name,
            "month":month,
            "salary":salary
        }
        emp_local_data.append(dict_value)
    return emp_local_data

def get_emp_list():
    data = frappe.db.sql("""select
                         emp.first_name as "first_name",emp.date_of_birth as "dob",emp.date_of_joining as "date_of_join" from `tabEmployee` emp
                         """,as_dict=True)
    print('data of empl : ',data)
    return data

