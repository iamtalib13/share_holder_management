// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Day Management Checkin", {
  refresh: function (frm) {
    if (frm.is_new()) {
      //employee id set on new form

      let user = frappe.session.user;
      let eid = user.match(/\d+/)[0];

      // Initialize the modified employee_id
      let modifiedEmployeeId = "";

      // Check if the user string contains "ABPS" or "MCPS"
      if (user.includes("ABPS")) {
        modifiedEmployeeId = "ABPS" + eid;
      } else if (user.includes("MCPS")) {
        modifiedEmployeeId = "MCPS" + eid;
      } else {
        // If neither "ABPS" nor "MCPS" is found, use the numeric part as is
        modifiedEmployeeId = eid;
      }

      // Set the "employee_id" field with the modified value
      frm.set_value("employee", modifiedEmployeeId);
      console.log("Employee :", frm.doc.employee);

      // Get branch value for the specified employee
      frappe.db.get_value(
        "Employee",
        { employee: frm.doc.employee },
        "branch",
        function (response) {
          if (response && response.branch) {
            // Set the branch field in your current form
            let branch = response.branch;
            frm.set_value("branch", response.branch);

            // Log the branch value to the console
            console.log("Branch:", frm.doc.branch);

            // Server Date and Time
            frm.call({
              method: "get_server_datetime",
              freeze: true, // Set to true to freeze the UI
              freeze_message: "Please wait, processing data...",
              callback: function (r) {
                if (!r.exc && r.message) {
                  frm.set_value("log_time", r.message);
                  frm.refresh_field("log_time");
                  console.log("branch client :", branch);
                  if (branch == "Gondia HO") {
                    console.log("Head Office");
                    frm.call({
                      method: "ho_day_start_and_end",
                      freeze: true, // Set to true to freeze the UI
                      freeze_message: "Please wait, processing data...",
                      args: {
                        branch: branch, // Only pass the branch filter
                      },
                      callback: function (r) {
                        if (!r.exc) {
                          // Successful response handling code
                          console.log("Success:", r.message);

                          if (r.message === "Day Completed") {
                            console.log("Day completed");
                            frm.set_df_property("log_type", "options", "");
                            frm.disable_save();
                            frm.disable_form();
                          } else if (r.message === "Day Not Ended") {
                            console.log("Day Not Ended");
                            frm.set_df_property("log_type", "options", "End");
                          } else if (r.message === "Day Not Started") {
                            console.log("Day Not Started");
                            // Set the options for the `primary_phone` select field
                            frm.set_df_property("log_type", "options", "Start");
                          }
                        } else {
                          // Error handling code
                          console.log("Error:", r.exc);
                        }
                      },
                    });
                  } else if (branch !== "Gondia HO") {
                    console.log("Branch");
                    frm.call({
                      method: "get_branch_checkin_details",
                      freeze: true, // Set to true to freeze the UI
                      freeze_message: "Please wait, processing data...",
                      args: {
                        branch: branch, // Only pass the branch filter
                      },
                      callback: function (r) {
                        if (!r.exc) {
                          // Successful response handling code
                          if (r.message === "Ho Day Completed") {
                            frappe.msgprint(
                              "Ho Day Completed. Perform actions accordingly."
                            );
                          } else if (r.message === "Ho Day Started") {
                            frm.set_intro(
                              "<b>Day Started from <b>" +
                                "Gondia Head office" +
                                "</b>" +
                                " for " +
                                "<b>" +
                                new Date(frm.doc.log_time).toLocaleDateString(
                                  "en-GB"
                                ), // Format to DD/MM/YYYY
                              "green" // Change the color as needed
                            );
                          } else if (r.message === "Ho Day Ended") {
                            frappe.msgprint(
                              "Ho Day Ended. Perform actions accordingly."
                            );
                          } else if (r.message === "Ho Not Started") {
                            frm.disable_save();
                            frm.disable_form();
                            frm.set_intro(
                              "<b>Day Not Started from <b>" +
                                "Gondia Head office" +
                                "</b>" +
                                " for " +
                                "<b>" +
                                new Date(frm.doc.log_time).toLocaleDateString(
                                  "en-GB"
                                ), // Format to DD/MM/YYYY
                              "red" // Change the color as needed
                            );
                            frm.disable_save();
                            frm.disable_form();
                          }
                        } else {
                          // Error handling code
                          frappe.msgprint("Error: " + r.exc);
                        }
                      },
                    });

                    frm.call({
                      method: "branch_day_start_and_end",
                      freeze: true, // Set to true to freeze the UI
                      freeze_message: "Please wait, processing data...",
                      args: {
                        branch: branch, // Only pass the branch filter
                      },
                      callback: function (r) {
                        if (!r.exc) {
                          // Successful response handling code
                          console.log("Success:", r.message);

                          if (r.message === "Day Completed") {
                            console.log("Day completed");
                            frm.set_df_property("log_type", "options", "");
                            frm.disable_save();
                            frm.disable_form();
                          } else if (r.message === "Day Not Ended") {
                            console.log("Day Not Ended");
                            frm.set_df_property("log_type", "options", "End");
                          } else if (r.message === "Day Not Started") {
                            console.log("Day Not Started");
                            // Set the options for the `primary_phone` select field
                            frm.set_df_property("log_type", "options", "Start");
                          }
                        } else {
                          // Error handling code
                          console.log("Error:", r.exc);
                        }
                      },
                    });
                  }
                  // Place the last call inside this callback
                } else {
                  // Handle the case where there is an error or no response
                  console.error(
                    "SERVER INTERNET ERROR ",
                    r.exc || "No response"
                  );
                }
              },
            });
          }
        }
      );

      //   frm.call({
      //     method: "get_checkin_details",
      //     callback: function (r) {
      //       if (!r.exc && r.message) {
      //         frm.set_value("log_time", r.message);
      //         frm.refresh_field("log_time");
      //       } else {
      //         // Handle the case where there is an error or no response
      //         console.error("SERVER INTERNET ERROR ", r.exc || "No response");
      //       }
      //     },
      //   });
    } else if (!frm.is_new()) {
      frm.set_intro(
        "<b>Day " +
          frm.doc.log_type +
          "</b>	 successfully from <b>" +
          frm.doc.branch +
          "</b>" +
          " for " +
          "<b>" +
          new Date(frm.doc.log_time).toLocaleDateString("en-GB"), // Format to DD/MM/YYYY
        "green" // Change the color as needed
      );

      //Successfully logged the start of the day at Gondia HO.

      frm.disable_form();
      frm.disable_save();
    }
  },
});