// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Share Application Report"] = {
  filters: [
    {
      fieldname: "from_date",
      label: "From Date",
      fieldtype: "Date",
      default: frappe.datetime.month_start(), // Default to start of the current month
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: "To Date",
      fieldtype: "Date",
      default: frappe.datetime.nowdate(), // Default to today's date
      reqd: 1,
    },
  ],
};
