// Copyright (c) 2023, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Application", {
  refresh(frm) {
    if (frm.is_new()) {
      // frm.call({
      //   method: "check_last_application_sr_no",
      //   args: {},
      //   callback: function (r) {
      //     // Check if the message array contains at least one object
      //     if (r.message) {
      //       // Log the response value to the console
      //       console.log("Response -----");
      //       console.log("Response:", r.message);

      //       frm.set_value("application_sr_no", r.message);
      //       frm.refresh_field("application_sr_no");

      //       // Do something else with the response, if needed
      //     } else {
      //       frappe.throw("Server Down . .");
      //       // Handle the case where there is no response
      //     }
      //   },
      // });

      if (frappe.user.has_role("System Manager")) {
        console.log("System Admin");
      } else if (frappe.user.has_role("Share Admin")) {
        console.log("Share Admin");
        frm.disable_save();
        frm.disable_form();
      } else if (frappe.user.has_role("Share User Creator")) {
        console.log("Share Executive & User Creator");
      } else if (frappe.user.has_role("Share Executive")) {
        console.log("Share Executive");
      } else if (frappe.user.has_role("Share User")) {
        console.log("Share User");
      } else {
      }
    }

    if (!frm.is_new()) {
      if (frappe.user.has_role("System Manager")) {
        console.log("System Admin");
      } else if (frappe.user.has_role("Share Admin")) {
        console.log("Share Admin");
        frm.disable_save();
        frm.disable_form();
      } else if (frappe.user.has_role("Share User Creator")) {
        console.log("Share Executive & User Creator");
        if (frm.doc.status == "Pending From HO") {
          frm.disable_save();
          frm
            .add_custom_button(__("Sanction"), function () {
              frappe.confirm(
                "Are you sure you want to Approve - <b>" +
                  frm.doc.customer_name +
                  "</b>",
                () => {
                  // action to perform if Yes is selected
                  frm.call({
                    method: "get_server_datetime",
                    callback: function (r) {
                      if (!r.exc && r.message) {
                        frm.set_value("sanction_date", r.message);
                        frm.refresh_field("sanction_date");
                        frm.set_value("status", "Sanctioned");
                        frm.refresh_field("status");
                        frm.save();
                      } else {
                        // Handle the case where there is an error or no response
                        console.error(
                          "SERVER INTERNET ERROR ",
                          r.exc || "No response"
                        );
                      }
                    },
                  });
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });

          // Add custom button for Rejection
          frm
            .add_custom_button(__("Reject"), function () {
              frappe.confirm(
                "Are you sure you want to Reject- <b>" +
                  frm.doc.customer_name +
                  "</b>",
                () => {
                  // action to perform if Yes is selected
                  frm.set_value("status", "Rejected");
                  frm.refresh_field("status");
                  console.log("Reject");
                  frm.save();
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#dc3545", // Set red color
              color: "#ffffff", // Set font color to white
            });
        } else if (
          frm.doc.status == "Sanctioned" ||
          frm.doc.status == "Rejected"
        ) {
          frm.disable_save();
          frm.disable_form();
        }
      } else if (frappe.user.has_role("Share Executive")) {
        console.log("Share Executive");

        if (frm.doc.status == "Submitted") {
          frm.disable_form();
          frm.disable_save();
          frm
            .add_custom_button(__("Receive"), function () {
              frappe.confirm(
                "Are you sure you want to Receive - <b>" +
                  frm.doc.customer_name +
                  "</b>",
                () => {
                  frm.call({
                    method: "get_server_datetime",
                    callback: function (r) {
                      if (!r.exc && r.message) {
                        frm.set_value("received_date", r.message);
                        frm.refresh_field("received_date");
                        frm.set_value("status", "Received");
                        frm.refresh_field("status");
                        frm.save();
                      } else {
                        // Handle the case where there is an error or no response
                        console.error(
                          "SERVER INTERNET ERROR ",
                          r.exc || "No response"
                        );
                      }
                    },
                  });
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });

          // Add custom button for Rejection
          frm
            .add_custom_button(__("Return To Branch"), function () {
              let d = new frappe.ui.Dialog({
                title: "Enter Return Remarks",
                fields: [
                  {
                    label: "Return Remarks",
                    fieldname: "return_remark",
                    fieldtype: "Small Text",
                    reqd: 1, // Set reqd property to make it mandatory
                  },
                ],
                size: "small", // small, large, extra-large
                primary_action_label: "Submit",
                primary_action: function () {
                  // Check if the return remarks field is provided
                  if (!d.fields_dict.return_remark.get_value()) {
                    frappe.msgprint(__("Please provide return remarks."));
                    return;
                  }

                  // Use the return remarks value as needed, for example, updating a field in the main form
                  frm.set_value(
                    "return_remark",
                    d.fields_dict.return_remark.get_value()
                  );

                  // Set the status field to "Return To Branch"
                  frm.set_value("status", "Return To Branch");

                  // Refresh the status field
                  frm.refresh_field("status");
                  frm.save();
                  // Additional logic if needed
                  console.log(
                    "Submitted return remarks:",
                    d.fields_dict.return_remark.get_value()
                  );

                  // Hide the dialog
                  d.hide();
                },
              });

              d.show();
            })
            .css({
              "background-color": "#dc3545", // Set red color
              color: "#ffffff", // Set font color to white
            });
        } else if (frm.doc.status == "Received") {
          frm.disable_form();
          frm.disable_save();
        } else if (frm.doc.status == "Return To Branch") {
          frm.trigger("return_intro");
          frm.disable_save();
          frm.disable_form();
        } else if (frm.doc.status == "Pending From HO") {
          frm.disable_save();
          frm
            .add_custom_button(__("Sanction"), function () {
              frappe.confirm(
                "Are you sure you want to Approve - <b>" +
                  frm.doc.customer_name +
                  "</b>",
                () => {
                  frm.call({
                    method: "get_server_datetime",
                    callback: function (r) {
                      if (!r.exc && r.message) {
                        frm.set_value("sanction_date", r.message);
                        frm.refresh_field("sanction_date");
                        frm.set_value("status", "Sanctioned");
                        frm.refresh_field("status");
                        frm.save();
                      } else {
                        // Handle the case where there is an error or no response
                        console.error(
                          "SERVER INTERNET ERROR ",
                          r.exc || "No response"
                        );
                      }
                    },
                  });
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });

          // Add custom button for Rejection
          frm
            .add_custom_button(__("Reject"), function () {
              frappe.confirm(
                "Are you sure you want to Reject- <b>" +
                  frm.doc.customer_name +
                  "</b>",
                () => {
                  // action to perform if Yes is selected
                  frm.set_value("status", "Rejected");
                  frm.refresh_field("status");
                  console.log("Reject");
                  frm.save();
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#dc3545", // Set red color
              color: "#ffffff", // Set font color to white
            });
        } else if (
          frm.doc.status == "Sanctioned" ||
          frm.doc.status == "Rejected"
        ) {
          frm.disable_save();
          frm.disable_form();
        }
      } else if (frappe.user.has_role("Share User")) {
        console.log("Share User");

        if (frm.doc.status == "Draft") {
          frm
            .add_custom_button(__("Submit"), function () {
              frappe.confirm(
                "Are you sure you want to submit the form to the Head-Office?",
                () => {
                  frm.set_value("status", "Submitted");
                  frm.refresh_field("status");

                  frm.save();
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });
        } else if (frm.doc.status == "Return To Branch") {
          frm.trigger("return_intro");

          frm
            .add_custom_button(__("Submit"), function () {
              frappe.confirm(
                "Are you sure you want to submit the form to the Head-Office?",
                () => {
                  frm.set_value("status", "Submitted");
                  frm.refresh_field("status");

                  frm.save();
                },
                () => {
                  // action to perform if No is selected
                }
              );
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });
        } else {
          frm.disable_save();
          frm.disable_form();
        }
      } else {
      }
    }

    // frm.trigger("set_base_share_amount");
    frm.trigger("set_share_application_amount");

    //when form submitted, the form will be locked it means not editable;
    if (frm.doc.status == "Submitted") {
      frm.trigger("set_form_lock");
    }
  },

  return_intro: function (frm) {
    frm.set_intro("<b>Return Remark : </b>" + frm.doc.return_remark, "red");
  },

  date_of_birth: function (frm) {
    // Get the date of birth from the form
    const dateOfBirth = frm.doc.date_of_birth;

    // Check if the date of birth is provided
    if (dateOfBirth) {
      // Convert date string to Date object
      const dob = frappe.datetime.str_to_obj(dateOfBirth);

      // Get the current date
      const currentDate = frappe.datetime.str_to_obj(
        frappe.datetime.get_today()
      );

      // Calculate the difference in years
      const age = currentDate.getFullYear() - dob.getFullYear();

      // Adjust the age if the birthday hasn't occurred yet this year
      if (
        currentDate.getMonth() < dob.getMonth() ||
        (currentDate.getMonth() === dob.getMonth() &&
          currentDate.getDate() < dob.getDate())
      ) {
        // Set the age field value and refresh the field
        frm.set_value("age", age - 1);
      } else {
        // Set the age field value and refresh the field
        frm.set_value("age", age);
      }

      // Refresh the age field in the form
      frm.refresh_field("age");
    } else {
      // Log a message if the date of birth is not provided
      console.log("Date of birth is not provided.");
    }
  },

  no_of_shares(frm) {},
  onload_post_render: function (frm) {
    let share_base_amount = 100;

    frm.fields_dict["no_of_shares"].$input.on("input", function (event) {
      var value = frm.fields_dict["no_of_shares"].get_value();
      console.log("Real-time input. No. of shares: ", value);

      // Check if the number of shares is zero
      if (value === 0) {
        frappe.throw("Number of shares cannot be 0");
        return;
      }

      // Perform the calculation
      var noOfShares = value || 0;
      var baseShareAmount = share_base_amount || 0;
      var applicationCharges = frm.doc.share_application_charges || 0;
      var totalAmount = noOfShares * baseShareAmount + applicationCharges;
      var totalBaseAmount = noOfShares * baseShareAmount;

      // Log the values used in the calculation
      console.log(
        "Calculation Inputs: No. of shares=",
        noOfShares,
        "Base Share Amount=",
        baseShareAmount,
        "Application Charges=",
        applicationCharges
      );

      // Set the calculated total amount back to the form
      frm.set_value("base_share_amount", totalBaseAmount);
      frm.refresh_field("base_share_amount");

      // Set the calculated total amount back to the form
      frm.set_value("tot_share_amt", totalAmount);
      frm.refresh_field("tot_share_amt");

      // Log the calculated total amount to the console
      console.log("Calculated Total Amount: ", totalAmount);
    });
  },
  // set_base_share_amount(frm) {
  //   frm.set_value("base_share_amount", 100);
  // },
  set_share_application_amount(frm) {
    frm.set_value("share_application_charges", 10);
  },

  set_form_lock(frm) {
    frm.set_read_only();
    frm.disable_form();
    frm.disable_save();
    frm.page.clear_primary_action();
  },
});
