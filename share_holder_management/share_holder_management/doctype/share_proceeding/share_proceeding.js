// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Proceeding", {
  refresh: function (frm) {
    if (frm.doc.response === "True") {
      // Split the proceeding date string by '-' to get year, month, and day
      var parts = frm.doc.proceeding_date.split("-");

      // Format the date as "DD-MM-YYYY"
      var formattedDate = parts[2] + "-" + parts[1] + "-" + parts[0];

      // Set the intro message with the formatted date
      frm.set_intro("Showing records for date - " + formattedDate, "green");
    }
    // Your refresh code here

    console.log("proceeding Date :", frm.doc.proceeding_date);

    frm.add_custom_button(
      __("Print"),
      function () {
        var printUrl = frappe.urllib.get_full_url(
          "/api/method/frappe.utils.weasyprint.download_pdf?" +
            "doctype=" +
            encodeURIComponent("Share Proceeding") +
            "&name=" +
            encodeURIComponent("Share Proceeding") +
            "&print_format=Proceeding Form" +
            "&letterhead=Proceeding Letter Head"
        );
        var newWindow = window.open(printUrl);
        console.log(printUrl); // Log the URL to the console
        // Additional logic if needed
      },
      __("Print")
    );
  },

  find_btn: function (frm) {
    let date = frm.doc.proceeding_date;

    if (frm.doc.response === "False") {
      frm.call({
        method: "show_proceeding_logs",
        freeze: true, // Set to true to freeze the UI
        freeze_message: "Please wait, processing data...",
        args: {
          proceeding_date: date, // Only pass the branch filter
        },
        callback: function (r) {
          if (!r.exc) {
            // Successful response handling code
            console.log("Success:", r.message);
            cur_frm.clear_table("proceeding_members");
            cur_frm.refresh_fields();

            if (r.message.length === 0) {
              frappe.msgprint("No records found.");
              console.log("No records found on ");
            } else {
              // Iterate over the response array and add each object as a child record
              for (let i = 0; i < r.message.length; i++) {
                let data = r.message[i];
                let row = frm.add_child("proceeding_members", {
                  date: data.sanction_date,
                  application_sr_no: data.application_sr_no,
                  share_holder_name: data.customer_name,
                  branch: data.branch,
                });
              }

              frm.refresh_field("proceeding_members");
              frm.set_value("response", "True");
              frm.save();
            }
          } else {
            // Error handling code
            console.log("Error:", r.exc);
          }
        },
      });
    } else {
      frappe.msgprint(
        "Already Showing records of date - ",
        frm.doc.proceeding_date
      );
    }
  },

  proceeding_date: function (frm) {
    cur_frm.clear_table("proceeding_members");
    cur_frm.refresh_fields();
    frm.set_value("response", "False");
    frm.save();
  },
});
