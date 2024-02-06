// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Proceeding", {
  refresh: function (frm) {
    // Your refresh code here
  },

  find_btn: function (frm) {
    frm.call({
      method: "show_proceeding_logs",
      freeze: true, // Set to true to freeze the UI
      freeze_message: "Please wait, processing data...",
      args: {
        proceeding_date: frm.doc.proceeding_date, // Only pass the branch filter
      },
      callback: function (r) {
        if (!r.exc) {
          // Successful response handling code
          console.log("Success:", r.message);
        } else {
          // Error handling code
          console.log("Error:", r.exc);
        }
      },
    });
  },
});
