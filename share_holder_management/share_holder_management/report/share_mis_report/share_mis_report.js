// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Share MIS Report"] = {
  filters: [
    {
      fieldname: "branch",
      label: __("Branch"),
      fieldtype: "Link",
      options: "Branch", // Assuming the Branch doctype is named "Branch"
      get_query: function () {
        return {
          filters: {
            // Add additional filters if needed
          },
        };
      },
    },
  ],
};
