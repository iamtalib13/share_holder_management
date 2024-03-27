// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Day Management Checkin", {
  refresh: function (frm) {
    frm.trigger("custom_home_button");
    //frm.trigger()
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

            // calling check_conditions method to fetch date of previous records or current
            frappe.call({
              method:
                "share_holder_management.share_holder_management.doctype.day_management.day_management.check_conditions",
              freeze: true, // Set to true to freeze the UI
              freeze_message: "Please wait, processing data...",
              callback: function (r) {
                if (!r.exc && r.message) {
                  const data = r.message;
                  console.log("result message:", data);
                  const originalDate = data[0].Date;
                  console.log("Original Date:", originalDate);

                  const originalDateParts = originalDate.split("-");
                  // Reformat the date as dd/mm/yyyy
                  const formattedOriginalDate =
                    originalDateParts[2] +
                    "/" +
                    originalDateParts[1] +
                    "/" +
                    originalDateParts[0];

                  const currentDateTime = new Date();
                  const currentHour = currentDateTime
                    .getHours()
                    .toString()
                    .padStart(2, "0");
                  const currentMinute = currentDateTime
                    .getMinutes()
                    .toString()
                    .padStart(2, "0");

                  const currentTime = currentHour + ":" + currentMinute;
                  console.log("current time format:", currentTime);

                  const formattedDateTime = originalDate + "," + currentTime;
                  console.log("formatted date and time:", formattedDateTime);

                  // Combine the original date and current time
                  const modifiedDate =
                    formattedOriginalDate + " " + currentTime;

                  console.log("final formatted date time:", modifiedDate);

                  //frm.set_value("log_time", modifiedDate);
                  // Convert the modified date to ISO 8601 format
                  const isoFormattedDateTime =
                    frappe.datetime.user_to_str(modifiedDate);

                  console.log("isoFormattedDateTime:", isoFormattedDateTime);

                  // Set the value of the log_time field
                  frm.set_value("log_time", isoFormattedDateTime);

                  // Refresh the log_time field
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
                        date: originalDate,
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
                        date: originalDate, // passing custom date fomat as yyyy-mm-dd
                      },
                      callback: function (r) {
                        if (!r.exc) {
                          // Successful response handling code
                          if (r.message === "Ho Day Completed") {
                            frappe.msgprint(
                              "Ho Day Completed. Perform actions accordingly."
                            );
                          } else if (r.message === "Ho Day Started") {
                            if (frm.doc.log_type) {
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
                            }
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
                        date: originalDate,
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

                  // Getting share application doc records
                  frm.call({
                    method: "check_share_records",
                    args: {
                      branch: branch,
                      application_date: originalDate,
                    },
                    callback: function (response) {
                      if (response && response.message) {
                        // Process the response data
                        const shareRecords = response.message;
                        console.log("Share Records:", shareRecords);

                        const flag = shareRecords.is_count_equal;
                        console.log("flag:", flag);
                        if (flag === "false") {
                          console.log("False hai");
                          frm.set_df_property("log_type", "options", "");
                          frm.disable_save();
                          // frm.disable_form();
                          frm.set_intro(
                            "<div style='display: inline-block; border-radius: 50%; width: 20px; height: 20px; background-color: yellow; color: black; text-align: center; line-height: 20px;'>&#9888;</div>" +
                              "<b> Day cannot end due to branch pending work. </b>",
                            "red"
                          );
                        }

                        // You can perform further actions here based on the retrieved data
                      } else {
                        // Handle error case
                        console.error("Error fetching share records.");
                      }
                    },
                  });
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

      // // Get branch value for the specified employee
      // frappe.db.get_value(
      //   "Employee",
      //   { employee: frm.doc.employee },
      //   "branch",
      //   function (response) {
      //     if (response && response.branch) {
      //       // Print branch value to console
      //       const branchName = response.branch;
      //       console.log("Branch second time:", branchName);
      //     }
      //   }
      // );
    } else if (!frm.is_new()) {
      frm
        .add_custom_button(
          '<span><img src="/files/home.png" alt="Home" style="width: 16px; height: 16px; vertical-align: middle;"> Home</span>',
          function () {
            frappe.set_route("/app/");
          }
        )
        .addClass("custom-button")
        .css({
          "background-color": "black",
          color: "white",
          "font-weight": "bold",
          border: "1px solid black",
          transition: "all 0.3s ease",
          padding: "5px 10px", // Adjust padding as needed
        })
        .hover(
          function () {
            $(this).css({
              "background-color": "white",
              color: "black",
              "border-color": "black",
            });
          },
          function () {
            $(this).css({
              "background-color": "black",
              color: "white",
              "border-color": "black",
            });
          }
        );
      frm.disable_form();
      frm.disable_save();
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

      //frm.disable_form();
      //frm.disable_save();
    }
  },

  after_save: function (frm) {
    if (frappe.user.has_role("Share Executive")) {
      frappe.set_route("/app/day-management");
    } else {
      setTimeout(function () {
        frappe.set_route("app/share-management");
      }, 1000); //  1 seconds
    }
  },
  before_save: function (frm) {
    let endlog = frm.doc.log_type;
    let branch = frm.doc.branch;

    if (endlog === "End" && branch === "Gondia HO") {
      frm.call({
        method: "start_end_details",
        args: {
          totalEndCount: 0,
          totalBranchCount: 0,
        },
        callback: function (r) {
          if (r.message) {
            let flag = r.flag;
            if (!flag) {
              frappe.validated = false;
              frappe.msgprint(
                "You cannot End HO until branches are not ended for the day."
              );
              frm.set_value("log_type", "");
            }
          }
        },
      });
    }
  },

  // before_save: function (frm) {
  //   let endlog = frm.doc.log_type;
  //   console.log("End Logtype:", endlog);

  // },

  custom_home_button(frm) {
    frm
      .add_custom_button(
        '<span><img src="/files/home.png" alt="Home" style="width: 16px; height: 16px; vertical-align: middle;"> Home</span>',
        function () {
          frappe.set_route("/app/");
        }
      )
      .addClass("custom-button")
      .css({
        "background-color": "black",
        color: "white",
        "font-weight": "bold",
        border: "1px solid black",
        transition: "all 0.3s ease",
        padding: "5px 10px", // Adjust padding as needed
      })
      .hover(
        function () {
          $(this).css({
            "background-color": "white",
            color: "black",
            "border-color": "black",
          });
        },
        function () {
          $(this).css({
            "background-color": "black",
            color: "white",
            "border-color": "black",
          });
        }
      );
    frm
      .add_custom_button(
        '<span><img src="/files/home.png" alt="Home" style="width: 16px; height: 16px; vertical-align: middle;"> Share Application</span>',
        function () {
          frappe.set_route("List", "Share Application");
        }
      )
      .addClass("custom-button")
      .css({
        "background-color": "black",
        color: "white",
        "font-weight": "bold",
        border: "1px solid black",
        transition: "all 0.3s ease",
        padding: "5px 10px", // Adjust padding as needed
      })
      .hover(
        function () {
          $(this).css({
            "background-color": "white",
            color: "black",
            "border-color": "black",
          });
        },
        function () {
          $(this).css({
            "background-color": "black",
            color: "white",
            "border-color": "black",
          });
        }
      );
  },
});
