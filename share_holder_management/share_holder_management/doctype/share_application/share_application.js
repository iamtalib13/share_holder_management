// Copyright (c) 2023, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Application", {
  before_save: function (frm) {},

  validate: function (frm) {
    // Check if the sanction date is blank or before 1/02/2024
    if (
      frm.doc.sanction_date &&
      frappe.datetime.str_to_obj(frm.doc.sanction_date) >
        frappe.datetime.str_to_obj("2024-02-01")
    ) {
      // Check if the child table is empty
      if (!frm.doc.nominee_details || frm.doc.nominee_details.length === 0) {
        frappe.throw("Please Add at Least One Nominee.");
      }
    }
  },

  refresh(frm) {
    frm.trigger("section_colors");

    frm.trigger("custom_file_upload");

    frm.trigger("child_table_controls");

    if (frm.is_new()) {
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

            frm.set_value("ac_open_dt", originalDate);
            frm.refresh_field("ac_open_dt");

            frm.set_value("application_date", originalDate);
            frm.refresh_field("application_date");
          }
        },
      });

      if (!frappe.user.has_role("System Manager")) {
        frm.call({
          method: "check_last_application_sr_no",
          args: {},
          callback: function (r) {
            // Check if the message array contains at least one object
            if (r.message) {
              var barcodeValue = String(r.message);
              frm.set_value("application_sr_no", r.message);

              frm.refresh_field("application_sr_no");

              // Do something else with the response, if needed
            } else {
              frappe.throw("Server Down . .");
              // Handle the case where there is no response
            }
          },
        });
        console.log("owner", frm.doc.owner);
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

              // Split the original date string
              var parts = originalDate.split("-");

              // Create a new date object using the parts
              var formattedDate = new Date(parts[0], parts[1] - 1, parts[2]);

              // Format the date as "DD-MM-YYYY"
              var formattedDateString = formattedDate.toLocaleDateString(
                "en-GB",
                {
                  day: "2-digit",
                  month: "2-digit",
                  year: "numeric",
                }
              );

              console.log("Formatted Date:", formattedDateString);

              frm.call({
                method: "check_branch_and_branch_code",
                args: {
                  owner: frm.doc.owner, // Pass owner directly instead of wrapping it in self
                },
                callback: function (r) {
                  // Check if the message array contains at least one object
                  if (r.message) {
                    frm.set_value("branch", r.message.branch);
                    frm.set_value("branch_code", r.message.branch_code);

                    let branch = r.message.branch;
                    frm.call({
                      method: "get_branch_checkin_details",
                      freeze: true, // Set to true to freeze the UI
                      freeze_message: "Please wait, processing data...",
                      args: {
                        branch: branch, // Only pass the branch filter
                        date: originalDate, //Date filter
                      },
                      callback: function (r) {
                        if (!r.exc) {
                          console.log("response:", r.message);

                          // Successful response handling code
                          if (r.message === "Day Start") {
                            console.log("day start");
                            frm.trigger("Intro_messages");
                          } else if (r.message === "Branch Day Ended") {
                            console.log("Branch Day Ended");
                            $(".form-page").css("display", "none");
                            frm.disable_save();
                            frm.disable_form();

                            frm.set_intro(
                              "<b>Day Ended from <b>" +
                                branch +
                                "</b>" +
                                " for " +
                                "<b>" +
                                formattedDateString,
                              "red" // Change the color as needed
                            );
                            frappe.msgprint({
                              message:
                                "Day has been Ended from branch. Please Go to Home page.",
                              // primary_action: {
                              //   label: __("OK"),
                              //   action: function () {
                              //     frappe.msgprint.hide(); // Hide the message
                              //   },
                              // },
                            });

                            frm.disable_save();
                            frm.disable_form();
                          } else if (r.message === "Branch Day Not Started") {
                            console.log(
                              "Branch Day Not Started and HO started"
                            );
                            $(".form-page").css("display", "none");
                            frm.disable_save();
                            frm.disable_form();
                            frm.set_intro(
                              " <u><a href='/app'> <- Go Back</a></u> <b>Day Not Started from <b>" +
                                branch +
                                "</b>" +
                                " for " +
                                "<b>" +
                                formattedDateString,
                              "red" // Change the color as needed
                            );

                            // // Message to be displayed in the dialog
                            // var message =
                            //   "Branch Day Not Started. Do you want to start?";

                            // // Create a Frappe dialog
                            // var dialog = new frappe.ui.Dialog({
                            //   title: "Start Branch Day",
                            //   fields: [
                            //     {
                            //       fieldtype: "HTML",
                            //       options: message,
                            //     },
                            //   ],
                            //   primary_action: function () {
                            //     // Redirect to the Day Management Checkin form
                            //     frappe.new_doc(
                            //       "Day Management Checkin",
                            //       function (doc) {
                            //         console.log("New document created:", doc);
                            //         frappe.set_route(
                            //           "Form",
                            //           "Day Management Checkin",
                            //           doc.name
                            //         );
                            //       }
                            //     );

                            //     dialog.hide();
                            //   },
                            //   primary_action_label: __("Yes"),
                            //   secondary_action_label: __("No"),
                            //   secondary_action: function () {
                            //     dialog.hide();
                            //   },
                            // });

                            // // Show the dialog
                            // dialog.show();

                            frm.disable_save();
                            frm.disable_form();
                          } else if (
                            r.message === "Branch and HO Day Not Started"
                          ) {
                            console.log("Branch and HO Day Not Started");
                            $(".form-page").css("display", "none");
                            frm.disable_save();
                            frm.disable_form();
                            frm.set_intro(
                              " <u><a href='/app'> <- Go Back</a></u> <b>Day Not Started from <b>" +
                                "Gondia HO & " +
                                branch +
                                "</b>" +
                                " for " +
                                "<b>" +
                                formattedDateString,
                              "red" // Change the color as needed
                            );
                            // frappe.msgprint(
                            //   "Gondia HO not started. Please Contact HO"
                            // );

                            frm.disable_save();
                            frm.disable_form();
                          }
                        } else {
                          // Error handling code
                          frappe.msgprint("Error: " + r.exc);
                        }
                      },
                    });

                    console.log("Client Branch :", branch);

                    frm.refresh_fields(["branch", "branch_code"]); // Refresh the fields

                    // Do something else with the response, if needed
                  } else {
                    frappe.throw("Server Down . .");
                    // Handle the case where there is no response
                  }
                },
              });
            }
          },
        });
      }

      if (frappe.user.has_role("System Manager")) {
        console.log("System Admin");
      } else if (frappe.user.has_role("Share Admin")) {
        console.log("Share Admin");
        //frm.disable_save();
        //frm.disable_form();
      } else if (frappe.user.has_role("Share User Creator")) {
        console.log("Share Executive & User Creator");
      } else if (frappe.user.has_role("Share Executive")) {
        console.log("Share Executive");
      } else if (frappe.user.has_role("Share User")) {
        console.log("Share User");
        frm.set_value("no_of_shares", 1);
        frm.refresh_field("no_of_shares");
        frm.set_df_property("no_of_shares", "read_only", 1);
      } else {
      }
    }

    if (!frm.is_new()) {
      if (frappe.user.has_role("System Manager")) {
        frm.add_custom_button(
          __("Receive"),
          function () {
            frappe.confirm(
              "Admin -> Receive?",
              () => {
                frm.set_value("status", "Received");
                frm.refresh_field("status");

                frm.save();
              },
              () => {
                // action to perform if No is selected
              }
            );
          },
          __("Admin")
        );
        frm.add_custom_button(
          __("Draft"),
          function () {
            frappe.confirm(
              "Admin -> Draft?",
              () => {
                frm.set_value("status", "Draft");
                frm.refresh_field("status");

                frm.save();
              },
              () => {
                // action to perform if No is selected
              }
            );
          },
          __("Admin")
        );

        console.log("System Admin");
      } else if (frappe.user.has_role("Share Admin")) {
        console.log("Share Admin");
        //frm.disable_save();
        //frm.disable_form();
      } else if (frappe.user.has_role("Share User Creator")) {
        console.log("Share Executive & User Creator");

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
        } else if (frm.doc.status == "Return To Branch") {
          frm.trigger("return_intro");
          frm.disable_save();
          frm.disable_form();
        } else if (
          frm.doc.status == "Pending From HO" ||
          frm.doc.status == "Received"
        ) {
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
        } else if (frm.doc.status == "Return To Branch") {
          frm.trigger("return_intro");
          frm.disable_save();
          frm.disable_form();
        } else if (
          frm.doc.status == "Pending From HO" ||
          frm.doc.status == "Received"
        ) {
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
        frm.set_df_property("no_of_shares", "read_only", 1);

        if (frm.doc.status == "Draft") {
          frm
            .add_custom_button(__("Submit"), function () {
              if (
                !frm.doc.nominee_details ||
                frm.doc.nominee_details.length === 0
              ) {
                frappe.throw("Please Add Nominee before submit");
              } else {
                let totalPercentage = 0;

                // Iterate through the child table to calculate the total percentage
                frm.doc.nominee_details.forEach(function (row) {
                  totalPercentage += row.nominee_share_percentage;
                });

                // Check if total percentage is greater than 100
                if (totalPercentage !== 100) {
                  frappe.throw("Total Nominee Share Percentage must be 100%.");
                } else {
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
                }
              }
            })
            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });
        } else if (frm.doc.status == "Return To Branch") {
          frm.trigger("return_intro");

          frm
            .add_custom_button(__("Submit"), function () {
              if (
                !frm.doc.nominee_details ||
                frm.doc.nominee_details.length === 0
              ) {
                frappe.throw("Please Add Nominee before submit");
              } else {
                let totalPercentage = 0;

                // Iterate through the child table to calculate the total percentage
                frm.doc.nominee_details.forEach(function (row) {
                  totalPercentage += row.nominee_share_percentage;
                });

                // Check if total percentage is greater than 100
                if (totalPercentage !== 100) {
                  frappe.throw("Total Nominee Share Percentage must be 100%.");
                } else {
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
                }
              }
            })

            .css({
              "background-color": "#28a745", // Set green color
              color: "#ffffff", // Set font color to white
            });
        } else if (frm.doc.status == "Submitted") {
          frm.set_intro(
            "<div style='display: inline-block; border-radius: 50%; width: 20px; height: 20px; background-color: green; color: white; text-align: center; line-height: 20px;'>&#10003;</div>" +
              "<b> Application is Submitted Successfully to Head Office </b>",
            "green"
          );
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

    frm.fields_dict.add_to_child.$input.css({
      "background-color": "black", // Set the background color to black
      color: "white", // Set the text color to white
      width: "100%", // Set width to 100%
      position: "relative", // Add position: relative
      padding: "10px", // Add padding for better visibility and aesthetics
      border: "none", // Remove border if needed
      cursor: "pointer", // Change cursor to pointer for better UX
    });
  },

  async custom_file_upload(frm) {
    frm.$wrapper.find(".mt-2 text-center").eq(1).hide(); // Hide the second button
    frm.$wrapper.find(".mt-2 text-center").eq(2).hide(); // Hide the third button
    frm.get_field("membership_form").df.options = {
      restrictions: {
        allowed_file_types: [".pdf", ".jpeg", ".jpg", ".png"],
      },
    };
    frm.get_field("payment_receipt").df.options = {
      restrictions: {
        allowed_file_types: [".pdf", ".jpeg", ".jpg", ".png"],
      },
    };
    frm.get_field("kyc").df.options = {
      restrictions: {
        allowed_file_types: [".pdf", ".jpeg", ".jpg", ".png"],
      },
    };
  },

  membership_form: function (frm) {
    // Get the value of the membership_form field
    var fileUrl = frm.doc.membership_form;

    // Extract the file extension
    var fileExtension = fileUrl.split(".").pop().toLowerCase();

    // Check the file type
    if (fileExtension === "jpg" || fileExtension === "jpeg") {
      console.log("JPEG file uploaded");
      frm.set_df_property(
        "membership_form",
        "description",
        "<b style='color:darkgreen;'>JPEG</b>"
      );
    } else if (fileExtension === "png") {
      console.log("PNG file uploaded");
      frm.set_df_property(
        "membership_form",
        "description",
        "<b style='color:darkgreen;'>PNG</b>"
      );
    } else if (fileExtension === "pdf") {
      console.log("PDF file uploaded");
      frm.set_df_property(
        "membership_form",
        "description",
        "<b style='color:darkgreen;'>PDF</b>"
      );
    } else {
      console.log("Unknown file type uploaded");
      frm.set_df_property(
        "membership_form",
        "description",
        "<b style='color:red;'>Only PDF/JPG/JPEG/PNG Supported</b>"
      );
      frm.set_value("membership_form", null);
    }
  },
  payment_receipt: function (frm) {
    // Get the value of the payment_receipt field
    var fileUrl = frm.doc.payment_receipt;

    // Extract the file extension
    var fileExtension = fileUrl.split(".").pop().toLowerCase();

    // Check the file type
    if (fileExtension === "jpg" || fileExtension === "jpeg") {
      console.log("JPEG file uploaded");
      frm.set_df_property(
        "payment_receipt",
        "description",
        "<b style='color:darkgreen;'>JPEG</b>"
      );
    } else if (fileExtension === "png") {
      console.log("PNG file uploaded");
      frm.set_df_property(
        "payment_receipt",
        "description",
        "<b style='color:darkgreen;'>PNG</b>"
      );
    } else if (fileExtension === "pdf") {
      console.log("PDF file uploaded");
      frm.set_df_property(
        "payment_receipt",
        "description",
        "<b style='color:darkgreen;'>PDF</b>"
      );
    } else {
      console.log("Unknown file type uploaded");
      frm.set_df_property(
        "payment_receipt",
        "description",
        "<b style='color:red;'>Only PDF/JPG/JPEG/PNG Supported</b>"
      );
      frm.set_value("payment_receipt", null);
    }
  },
  kyc: function (frm) {
    // Get the value of the kyc field
    var fileUrl = frm.doc.kyc;

    // Extract the file extension
    var fileExtension = fileUrl.split(".").pop().toLowerCase();

    // Check the file type
    if (fileExtension === "jpg" || fileExtension === "jpeg") {
      console.log("JPEG file uploaded");
      frm.set_df_property(
        "kyc",
        "description",
        "<b style='color:darkgreen;'>JPEG</b>"
      );
    } else if (fileExtension === "png") {
      console.log("PNG file uploaded");
      frm.set_df_property(
        "kyc",
        "description",
        "<b style='color:darkgreen;'>PNG</b>"
      );
    } else if (fileExtension === "pdf") {
      console.log("PDF file uploaded");
      frm.set_df_property(
        "kyc",
        "description",
        "<b style='color:darkgreen;'>PDF</b>"
      );
    } else {
      console.log("Unknown file type uploaded");
      frm.set_df_property(
        "kyc",
        "description",
        "<b style='color:red;'>Only PDF/JPG/JPEG/PNG Supported</b>"
      );
      frm.set_value("kyc", null);
    }
  },

  child_table_controls(frm) {
    frm.fields_dict["nominee_details"].grid.wrapper
      .find(".grid-add-row")
      .hide();
  },

  Intro_messages(frm) {
    // Construct the intro message with the "Home" link aligned to the right
    var introMessage =
      "<div style='display: flex; align-items: center; justify-content: space-between;'>";

    // Display "Please Submit your Form" message if document is in "Draft" status, aligned to the left
    if (frm.doc.status == "Draft" && !frm.is_new()) {
      introMessage +=
        "<span style='float: left; color: blue;'>Please Submit your Form</span>";
    } else if (frm.doc.status == "Draft" && frm.is_new()) {
      introMessage +=
        "<span style='float: left; color: blue;'>Please Fill <span style='color: red;'>*</span> All Mandatory fields</span>";
    }

    introMessage += "</div>";

    // Set the intro message
    frm.set_intro(introMessage);
  },

  section_colors(frm) {
    //buttons

    frm.fields_dict["nominee_form_section"].wrapper.css(
      "background-color",
      "antiquewhite"
    );

    // Lightened blue for "ac_information_section"
    frm.fields_dict["ac_information_section"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened blue
    );

    // Lightened lavender for "no_of_share_section"
    frm.fields_dict["no_of_share_section"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );

    // Lightened mint green for "after_sanction_share_ac_information_section"
    frm.fields_dict["after_sanction_share_ac_information_section"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened mint green
    );

    frm.fields_dict["nominee_table_section"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened mint green
    );

    //Personal Information Tab

    frm.fields_dict["acc_section_details"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened mint green
    );

    frm.fields_dict["personal_information_section"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );
    frm.fields_dict["location_section"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened mint green
    );

    frm.fields_dict["kyc_section"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );

    frm.fields_dict["kyc_section_2"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );

    //Divident Tab

    frm.fields_dict["divident_section_1"].wrapper.css(
      "background-color",
      "#DCF2F1" // Hex color code for the lightened mint green
    );

    frm.fields_dict["personal_information_section"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );
    frm.fields_dict["remark_section"].wrapper.css(
      "background-color",
      "#F5EEE6" // Hex color code for the lightened lavender
    );
  },

  test_details_add: function (frm) {},

  return_intro: function (frm) {
    frm.set_intro("<b>Return Remark : </b>" + frm.doc.return_remark, "red");
  },

  // date_of_birth: function (frm) {
  //   // Get the date of birth from the form
  //   const dateOfBirth = frm.doc.date_of_birth;
  //   console.log(dateOfBirth);
  //   // Check if the date of birth is provided
  //   if (dateOfBirth) {
  //     // Convert date string to Date object
  //     const dob = frappe.datetime.str_to_obj(dateOfBirth);

  //     // Get the current date
  //     const currentDate = frappe.datetime.str_to_obj(
  //       frappe.datetime.get_today()
  //     );

  //     // Calculate the difference in years
  //     const age = currentDate.getFullYear() - dob.getFullYear();

  //     // Adjust the age if the birthday hasn't occurred yet this year
  //     if (
  //       currentDate.getMonth() < dob.getMonth() ||
  //       (currentDate.getMonth() === dob.getMonth() &&
  //         currentDate.getDate() < dob.getDate())
  //     ) {
  //       // Set the age field value and refresh the field
  //       frm.set_value("age", age - 1);
  //       frm.refresh_field("age");
  //     } else {
  //       // Set the age field value and refresh the field
  //       frm.set_value("age", age);

  //       frm.refresh_field("age");
  //     }

  //     // Refresh the age field in the form
  //     frm.refresh_field("age");
  //   } else {
  //     // Log a message if the date of birth is not provided
  //     console.log("Date of birth is not provided.");
  //   }
  // },

  // arshad changes
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
      let age = currentDate.getFullYear() - dob.getFullYear();
      console.log("current", currentDate.getFullYear());
      console.log("dob", dob.getFullYear());

      console.log("age is ", age);

      // Check if age is less than 18
      {
        // Adjust the age if the birthday hasn't occurred yet this year
        if (
          currentDate.getMonth() < dob.getMonth() ||
          (currentDate.getMonth() === dob.getMonth() &&
            currentDate.getDate() < dob.getDate())
        ) {
          // Set the age field value and refresh the field
          age = age - 1;
          if (age < 18) {
            // Show message for age less than 18
            frm.set_value("age", "");
            frm.set_value("date_of_birth", null);
            frappe.msgprint(__("Age should be 18 or above."));
            // Clear both age and date_of_birth fields
            frm.refresh_field("age");
            frm.refresh_field("date_of_birth");
          } else {
            frm.set_value("age", age);
            frm.refresh_field("age");
          }
        } else {
          // Set the age field value and refresh the field
          age = age;
          if (age < 18) {
            // Show message for age less than 18
            frm.set_value("age", "");
            frm.set_value("date_of_birth", null);
            frappe.msgprint(__("Age should be 18 or above."));
            // Clear both age and date_of_birth fields
            frm.refresh_field("age");
            frm.refresh_field("date_of_birth");
          } else {
            frm.set_value("age", age);
            frm.refresh_field("age");
          }
        }
      }
    } else {
      // Log a message if the date of birth is not provided
      console.log("Date of birth is not provided.");
    }
  },

  no_of_shares(frm) {},

  nominee_age: function (frm) {
    console.log(frm.doc.nominee_age);
    if (frm.doc.nominee_age < 18) {
      frm.set_value("minor", 1);
      frm.refresh_field("minor");
    } else {
      frm.set_value("minor", 0);
      frm.refresh_field("minor");
    }
  },

  onload_post_render: function (frm) {
    let share_base_amount = 10;

    frm.fields_dict["no_of_shares"].$input.on("input", function (event) {
      var value = frm.fields_dict["no_of_shares"].get_value();

      if (isNaN(value)) {
        frappe.throw(__("Please enter only numbers (0-9)."));

        frm.set_value("no_of_shares", null);
        frm.refresh_field("no_of_shares");
        return;
      }

      var noOfShares = parseFloat(value) || 0;
      console.log("Real-time input. No. of shares: ", noOfShares);

      if (noOfShares === 0) {
        frappe.throw("Number of shares cannot be 0");
        return;
      }

      var baseShareAmount = share_base_amount || 0;
      var applicationCharges = frm.doc.share_application_charges || 0;
      var totalAmount = noOfShares * baseShareAmount + applicationCharges;
      var totalBaseAmount = noOfShares * baseShareAmount;

      console.log(
        "Calculation Inputs: No. of shares=",
        noOfShares,
        "Base Share Amount=",
        baseShareAmount,
        "Application Charges=",
        applicationCharges
      );

      frm.set_value("base_share_amount", totalBaseAmount);
      frm.refresh_field("base_share_amount");

      frm.set_value("tot_share_amt", totalAmount);
      frm.refresh_field("tot_share_amt");

      console.log("Calculated Total Amount: ", totalAmount);
    });

    frm.fields_dict["no_of_shares"].$input.on("keydown", function (event) {
      var key = event.key;

      if (key === "Backspace") {
        // Handle Backspace key
        frm.set_value("base_share_amount", null);
        frm.set_value("tot_share_amt", null);
      }

      // Allow only numeric keys (0-9) and Backspace
      if (!(key >= "0" && key <= "9") && key !== "Backspace") {
        event.preventDefault();
      }
    });

    frm.fields_dict["nominee_share_percentage"].$input.on(
      "keydown",
      function (event) {
        var key = event.key;
        var currentValue =
          frm.fields_dict["nominee_share_percentage"].get_value();

        // Allow delete, backspace, right arrow, and left arrow keys
        if (
          key === "Delete" ||
          key === "Backspace" ||
          key === "ArrowRight" ||
          key === "ArrowLeft"
        ) {
          return;
        }

        // Prevent Tab key by keycode and key value
        if (event.keyCode === 9 || key === "Tab") {
          return;
        }

        // Check if the current value is already 100%
        if (parseInt(currentValue) >= 100 && key !== "Backspace") {
          event.preventDefault();
          return;
        }

        // Prevent typing if the value would exceed 100%
        if (parseInt(currentValue + key) > 100) {
          event.preventDefault();
        }
      }
    );

    // Logic for 'aadhaar_number' field
    frm.fields_dict["aadhaar_number"].$input.on("keydown", function (event) {
      var key = event.key;
      var aadhaarField = frm.fields_dict["aadhaar_number"];
      var value = aadhaarField.get_value();
      var regex = /^[0-9]+$/;

      // Allow right arrow, left arrow, delete key, and backspace
      if (
        key === "ArrowRight" ||
        key === "ArrowLeft" ||
        key === "Delete" ||
        key === "Backspace"
      ) {
        return;
      }

      // Check if the current length is already 12
      if (value.length >= 12 && key >= "0" && key <= "9") {
        event.preventDefault();
        return;
      }

      // Validate that only numbers are allowed
      if (!(key >= "0" && key <= "9")) {
        event.preventDefault();
        return;
      }

      // Validate the entire input against the regex
      if (!regex.test(value)) {
        frm.set_value("aadhaar_number", null);
        frm.refresh_field("aadhaar_number");
      }
    });

    // Allow both uppercase and lowercase alphabets, and 0-9 numbers
    frm.fields_dict["pan_no"].$input.on("input", function () {
      var value = frm.fields_dict["pan_no"].get_value();

      // Convert input to uppercase
      value = value.toUpperCase();

      // Validate that only uppercase alphabets and numbers are allowed
      var regex = /^[A-Z0-9]+$/;

      // Remove any characters that do not match the pattern
      var sanitizedValue = value.replace(new RegExp(`[^A-Z0-9]`, "g"), "");

      // Set the sanitized value back to the field
      frm.fields_dict["pan_no"].set_input(sanitizedValue);
    });
    frm.fields_dict["nominee_share_percentage"].$input.on(
      "keydown",
      function (event) {
        var key = event.key;

        // Allow numeric keys (0-9), Backspace, and Left/Right Arrow keys
        if (
          !(key >= "0" && key <= "9") &&
          key !== "Backspace" &&
          key !== "ArrowLeft" &&
          key !== "ArrowRight"
        ) {
          event.preventDefault();
        }
      }
    );

    frm.fields_dict["nominee_age"].$input.on("keydown", function (event) {
      var key = event.key;

      // Check if Backspace is pressed
      if (key === "Backspace") {
        // Get the current entered age
        var currentAge = frm.fields_dict["nominee_age"].get_value();

        // Check if the entered age is less than 18
        if (parseInt(currentAge) > 18) {
          console.log("Not a Minor");
        } else {
          console.log("Minor");
        }

        return; // Allow Backspace without further processing
      }

      // Allow numeric keys (0-9), and Left/Right Arrow keys
      if (
        !(key >= "0" && key <= "9") &&
        key !== "ArrowLeft" &&
        key !== "ArrowRight"
      ) {
        event.preventDefault();
      }

      // Get the entered age
      var age = parseInt(frm.fields_dict["nominee_age"].get_value() + key);

      // Check if the entered age is 18 or more
      if (age >= 18) {
        console.log("Not a Minor");
      } else {
        console.log("Minor");
      }
    });

    frm.fields_dict["nominee_age"].$input.on("input", function (event) {
      var key = event.key;

      // Check if Backspace is pressed
      if (key === "Backspace") {
        // Get the current entered age
        var currentAge = frm.fields_dict["nominee_age"].get_value();

        // Check if the entered age is less than 18
        if (parseInt(currentAge) > 18) {
          console.log("Not a Minor");
        } else {
          console.log("Minor");
        }

        return; // Allow Backspace without further processing
      }
    });

    // Logic for 'aadhaar_number' field
    frm.fields_dict["nominee_mobile_number"].$input.on(
      "keydown",
      function (event) {
        var key = event.key;
        var mobileField = frm.fields_dict["nominee_mobile_number"];

        // Check if the current length is already 10
        if (mobileField.get_value().length >= 10 && key >= "0" && key <= "9") {
          event.preventDefault();
          return;
        }

        // Validate that only numbers are allowed
        var regex = /^[0-9]+$/;

        // Allow only numeric keys (0-9), Backspace, Delete, Right Arrow, and Left Arrow
        if (
          !(key >= "0" && key <= "9") &&
          key !== "Backspace" &&
          key !== "Delete" &&
          key !== "ArrowRight" &&
          key !== "ArrowLeft"
        ) {
          event.preventDefault();
          return;
        }

        // Validate the entire input against the regex
        var value = mobileField.get_value();
        if (!regex.test(value)) {
          frm.set_value("nominee_mobile_number", null);
          frm.refresh_field("nominee_mobile_number");
        }
      }
    );

    frm.fields_dict["customer_id"].$input.on("keydown", function (event) {
      var key = event.key;

      // Validate that only numbers, right arrow, and left arrow are allowed
      var regex = /^[0-9]+$/;

      // Allow only numeric keys (0-9), Right Arrow, Left Arrow, and Backspace
      if (
        !(
          (key >= "0" && key <= "9") ||
          key === "ArrowRight" ||
          key === "ArrowLeft" ||
          key === "Backspace"
        )
      ) {
        event.preventDefault();
      }
    });

    frm.fields_dict["mobile"].$input.on("keydown", function (event) {
      var key = event.key;
      var mobileField = frm.fields_dict["mobile"];

      // Check if the current length is already 10
      if (mobileField.get_value().length >= 10 && key >= "0" && key <= "9") {
        event.preventDefault();
        return;
      }

      // Validate that only numbers, right arrow, left arrow, delete, and backspace are allowed
      var regex = /^[0-9]+$/;

      // Allow only numeric keys (0-9), Right Arrow, Left Arrow, Delete, and Backspace
      if (
        !(
          (key >= "0" && key <= "9") ||
          key === "ArrowRight" ||
          key === "ArrowLeft" ||
          key === "Delete" ||
          key === "Backspace"
        )
      ) {
        event.preventDefault();
        return;
      }
    });
    frm.fields_dict["customer_name"].$input.on("keydown", function (event) {
      var currentValue = frm.fields_dict["customer_name"].get_value();

      // Convert lowercase characters to uppercase
      if (event.key >= "a" && event.key <= "z") {
        currentValue += event.key.toUpperCase();
        frm.fields_dict["customer_name"].set_input(currentValue);
        event.preventDefault(); // Prevent the lowercase character from being added
      }

      // Validate that only uppercase alphabets, space, right arrow, left arrow, and delete are allowed
      var regex = /^[A-Z\s]+$/;

      // Allow only uppercase alphabet keys (A-Z), space, Right Arrow, Left Arrow, Backspace, and Delete
      if (
        !(
          (event.key >= "A" && event.key <= "Z") ||
          event.key === " " ||
          event.key === "ArrowRight" ||
          event.key === "ArrowLeft" ||
          event.key === "Backspace" ||
          event.key === "Delete"
        )
      ) {
        event.preventDefault();
      }
    });

    // Assuming moment.js is available
    frm.fields_dict["date_of_birth"].$input.on("input", function () {
      //console.log("working");
    });

    frm.fields_dict["nominee_fullname"].$input.on("keydown", function (event) {
      var key = event.key;

      // Validate that only alphabets, space, right arrow, and left arrow are allowed
      var regex = /^[a-zA-Z\s]+$/;

      // Allow only alphabet keys (a-z, A-Z), space, Right Arrow, Left Arrow, and Backspace
      if (
        !(
          (key >= "a" && key <= "z") ||
          (key >= "A" && key <= "Z") ||
          key === " " ||
          key === "ArrowRight" ||
          key === "ArrowLeft" ||
          key === "Backspace"
        )
      ) {
        event.preventDefault();
      }
    });
    frm.fields_dict["taluka"].$input.on("keydown", function (event) {
      var key = event.key;

      // Validate that only alphabets, space, right arrow, and left arrow are allowed
      var regex = /^[a-zA-Z\s]+$/;

      // Allow only alphabet keys (a-z, A-Z), space, Right Arrow, Left Arrow, and Backspace
      if (
        !(
          (key >= "a" && key <= "z") ||
          (key >= "A" && key <= "Z") ||
          key === " " ||
          key === "ArrowRight" ||
          key === "ArrowLeft" ||
          key === "Backspace"
        )
      ) {
        event.preventDefault();
      }
    });
    frm.fields_dict["city"].$input.on("keydown", function (event) {
      var key = event.key;

      // Validate that only alphabets, space, right arrow, and left arrow are allowed
      var regex = /^[a-zA-Z\s]+$/;

      // Allow only alphabet keys (a-z, A-Z), space, Right Arrow, Left Arrow, and Backspace
      if (
        !(
          (key >= "a" && key <= "z") ||
          (key >= "A" && key <= "Z") ||
          key === " " ||
          key === "ArrowRight" ||
          key === "ArrowLeft" ||
          key === "Backspace"
        )
      ) {
        event.preventDefault();
      }
    });

    frm.fields_dict["saving_current_ac_no"].$input.on(
      "keydown",
      function (event) {
        var key = event.key;

        // Validate that only numbers, right arrow, and left arrow are allowed
        var regex = /^[0-9]+$/;

        // Allow only numeric keys (0-9), Right Arrow, Left Arrow, and Backspace
        if (
          !(
            (key >= "0" && key <= "9") ||
            key === "ArrowRight" ||
            key === "ArrowLeft" ||
            key === "Backspace"
          )
        ) {
          event.preventDefault();
        }
      }
    );
  },
  customer_id: function (frm) {
    var cust_id = frm.doc.customer_id;

    // Check if a Share Application document exists with the given customer_id
    if (cust_id) {
      frm.call({
        method: "get_existing_customer",
        args: {
          customer_id: cust_id,
        },
        callback: function (response) {
          var customer_exists = response.message;

          console.log("Customer exists:", customer_exists);
          if (customer_exists == "True") {
            frm.set_df_property(
              "customer_id",
              "description",
              "<b style='color:darkgreen;'>Old-Customer</b>"
            );
          } else if (customer_exists == "False") {
            frm.set_df_property(
              "customer_id",
              "description",
              "<b style='color:orange;'>New-Customer</b>"
            );
          }
        },
      });
    } else {
      frm.set_df_property(
        "customer_id",
        "description",
        "<b style='color:red;'>Enter Customer ID</b>"
      );
    }
  },

  nominee_mobile_number: function (frm) {
    let mobile_no = frm.doc.nominee_mobile_number;
    let length = mobile_no ? mobile_no.length : 0;

    if (mobile_no) {
      if (length === 10) {
        frm.set_df_property(
          "nominee_mobile_number",
          "description",
          `<b style='color:green;'>Valid Phone Number (Length: ${length})</b>`
        );
      } else {
        frm.set_df_property(
          "nominee_mobile_number",
          "description",
          `<b style='color:red;'>Invalid Phone Number. Please enter 10 digits. (Length: ${length})</b>`
        );
      }
    } else {
      frm.set_df_property(
        "nominee_mobile_number",
        "description",
        `<b style='color:red;'>Please Enter 10 Digit Phone No. (Length: ${length})</b>`
      );
    }
  },

  mobile: function (frm) {
    let mobile_no = frm.doc.mobile;
    let length = mobile_no ? mobile_no.length : 0;

    if (mobile_no) {
      if (length === 10) {
        frm.set_df_property(
          "mobile",
          "description",
          `<b style='color:green;'>Valid Phone Number (Length: ${length})</b>`
        );
      } else {
        frm.set_df_property(
          "mobile",
          "description",
          `<b style='color:red;'>Invalid Phone Number. Please enter 10 digits. (Length: ${length})</b>`
        );
      }
    } else {
      frm.set_df_property(
        "mobile",
        "description",
        `<b style='color:red;'>Please Enter 10 Digit Phone No. (Length: ${length})</b>`
      );
    }
  },

  email_id: function (frm) {
    let email = frm.doc.email_id;
    if (email) {
      let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (emailPattern.test(email)) {
        frm.set_df_property(
          "email_id",
          "description",
          "<b style='color:green;'>Valid Email Address</b>"
        );
      } else {
        frm.set_df_property(
          "email_id",
          "description",
          "<b style='color:red;'>Invalid Email Address</b>"
        );
      }
    } else {
      frm.set_df_property(
        "email_id",
        "description",
        "<b style='color:red;'>Please Enter Email Address</b>"
      );
    }
  },

  aadhaar_number: function (frm) {
    let aadhar = frm.doc.aadhaar_number;
    let length = aadhar ? aadhar.length : 0;

    if (aadhar) {
      if (aadhar.length === 12 && /^\d+$/.test(aadhar)) {
        frm.set_df_property(
          "aadhaar_number",
          "description",
          `<b style='color:green;'>Valid Aadhar Number (Length: ${length})</b>`
        );
      } else {
        frm.set_df_property(
          "aadhaar_number",
          "description",
          `<b style='color:red;'>Invalid Aadhar Number. Please enter 12 digits. (Length: ${length})</b>`
        );
      }
    } else {
      frm.set_df_property(
        "aadhaar_number",
        "description",
        `<b style='color:red;'>Please Enter 12 Digit Aadhar No. (Length: ${length})</b>`
      );
    }
  },

  pan_no: function (frm) {
    let panNo = frm.doc.pan_no;
    if (panNo) {
      let panPattern = /^[A-Z]{5}\d{4}[A-Z]{1}$/;
      if (panPattern.test(panNo)) {
        frm.set_df_property(
          "pan_no",
          "description",
          "<b style='color:green;'>Valid PAN Number</b>"
        );
      } else {
        frm.set_df_property(
          "pan_no",
          "description",
          "<b style='color:red;'>Invalid PAN Number. It should be in the format: ABCDE1234F</b>"
        );
      }
    } else {
      frm.set_df_property(
        "pan_no",
        "description",
        "<b style='color:red;'>Please Enter PAN Number</b>"
      );
    }
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
  add_to_child: function (frm) {
    let nominee_fullname = frm.doc.nominee_fullname;
    let nominee_address = frm.doc.nominee_address;
    let nominee_relation = frm.doc.nominee_relation;
    let nominee_contact = frm.doc.nominee_mobile_number;
    let nominee_share = frm.doc.nominee_share_percentage;
    let nominee_age = frm.doc.nominee_age;
    let nominee_guardian_name = frm.doc.nominee_guardian_name;
    let nominee_minor = frm.doc.minor;

    if (!nominee_fullname) {
      frappe.throw("Please fill in the nominee's full name.");
    } else if (!nominee_relation) {
      frappe.throw("Please fill in the nominee's relation.");
    } else if (!nominee_share) {
      frappe.throw("Please fill in the nominee's share.");
    } else if (!nominee_age) {
      frappe.throw("Please fill in the nominee's age.");
    } else if (nominee_contact && nominee_contact.length !== 10) {
      frappe.throw("Nominee Contact Number must be 10 digits");
    } else if (nominee_share > 100) {
      frappe.throw("Share Percentage cannot be more than 100%");
    } else {
      let totalPercentage = 0;
      // Calculate the total percentage in the child table
      // Calculate the total percentage in the child table
      if (frm.doc.nominee_details && frm.doc.nominee_details.length > 0) {
        frm.doc.nominee_details.forEach(function (row) {
          totalPercentage += row.nominee_share_percentage;
        });
      }

      let remainingPercentage = 100 - totalPercentage;

      if (remainingPercentage <= 0) {
        frappe.throw("You have already added share percentage to 100 %");
      } else if (nominee_share > remainingPercentage) {
        frappe.throw(`You can add ${remainingPercentage}% only.`);
      } else {
        if (nominee_age < 18) {
          nominee_minor = 1; // Assuming you want to set nominee_minor to 1 if nominee_age is less than 18
        } else {
          nominee_minor = 0; // Assuming you want to set nominee_minor to 0 if nominee_age is 18 or above
        }

        let row = frm.add_child("nominee_details", {
          nominee_name: nominee_fullname,
          nominee_address: nominee_address,
          nominee_relation: nominee_relation,
          nominee_mobile_number: nominee_contact,
          nominee_share_percentage: nominee_share,
          nominee_age: nominee_age,
          minor: nominee_minor,
          nominee_guardian_name: nominee_guardian_name,
        });

        frm.refresh_field("nominee_details");
        frm.set_value("nominee_fullname", "");
        frm.set_value("nominee_guardian_name", "");
        frm.set_value("nominee_address", "");
        frm.set_value("nominee_relation", "");
        frm.set_value("nominee_mobile_number", "");
        frm.set_value("nominee_share_percentage", "");
        frm.set_value("nominee_age", "");
        frm.set_value("minor", 0); // Assuming you want to set nominee_minor to 0 after adding to child table
        if (!frm.is_new()) {
          frm.save();
        }
      }
    }
  },

  check_table: function (frm) {
    // Check if the child table is empty
    if (!frm.doc.nominee_details || frm.doc.nominee_details.length === 0) {
      frappe.msgprint("The child table is empty.");
    } else if (
      frm.doc.nominee_details ||
      frm.doc.nominee_details.length !== 0
    ) {
      let totalPercentage = 0;

      // Iterate through the child table to calculate the total percentage
      frm.doc.nominee_details.forEach(function (row) {
        totalPercentage += row.nominee_share_percentage;
      });

      // Check if total percentage is greater than 100
      if (totalPercentage > 100) {
        frappe.throw(
          "Total Nominee Share Percentage cannot be greater than 100."
        );
      }
    } else {
      let totalPercentage = 0;

      // Iterate through the child table to calculate the total percentage
      frm.doc.nominee_details.forEach(function (row) {
        totalPercentage += row.nominee_share_percentage;
      });

      // Check if total percentage is greater than 100
      if (totalPercentage > 100) {
        frappe.msgprint(
          "Total Nominee Share Percentage cannot be greater than 100."
        );
      } else {
        // Print the total percentage to the console and in msgprint
        console.log("Total Nominee Share Percentage:", totalPercentage);
        frappe.msgprint("Total Nominee Share Percentage: " + totalPercentage);
      }
    }
  },
});

frappe.ui.form.on("Share Application", {
  refresh(frm) {
    if (!frm.is_new()) {
      if (frappe.user.has_role("System Manager")) {
        // Additional logic for System Manager role
        frm.trigger("share_application_english_print");
        frm.trigger("share_application_hindi_print");
        frm.trigger("share_application_marathi_print");
        frm.trigger("share_application_default_print");
        frm.trigger("share_certificate_print");
      } else if (
        frappe.user.has_role("Share Admin") ||
        frappe.user.has_role("Share User Creator") ||
        frappe.user.has_role("Share Executive")
      ) {
        frm.trigger("share_application_default_print");
        frm.trigger("share_application_english_print");
        frm.trigger("share_application_hindi_print");
        frm.trigger("share_application_marathi_print");

        if (frm.doc.status === "Sanctioned") {
          frm.trigger("share_certificate_print");
        }
      } else if (frappe.user.has_role("Share User")) {
        if (frm.doc.status === "Sanctioned") {
          frm.trigger("share_certificate_print");
        }
      }

      // Set button types
      frm.set_df_property("Print", "button_type", "success");
      frm.set_df_property("Print-Hin", "button_type", "primary");
      frm.set_df_property("Print-Mar", "button_type", "warning");
    }
    frm.trigger("custome_home_button");
  },

  share_application_english_print(frm) {
    frm.add_custom_button(
      __("English"),
      function () {
        var printUrl = frappe.urllib.get_full_url(
          "/api/method/frappe.utils.weasyprint.download_pdf?" +
            "doctype=" +
            encodeURIComponent("Share Application") +
            "&name=" +
            encodeURIComponent(frm.doc.name) +
            "&print_format=Share English Form" +
            "&letterhead=Share Head English"
        );
        var newWindow = window.open(printUrl);
        console.log(printUrl); // Log the URL to the console
        // Additional logic if needed
      },
      __("Lang-Print")
    );
  },

  share_application_hindi_print(frm) {
    frm.add_custom_button(
      __("Hindi"),
      function () {
        var printUrl = frappe.urllib.get_full_url(
          "/api/method/frappe.utils.weasyprint.download_pdf?" +
            "doctype=" +
            encodeURIComponent("Share Application") +
            "&name=" +
            encodeURIComponent(frm.doc.name) +
            "&print_format=Share Hindi Form" +
            "&letterhead=Share Head Hindi"
        );
        var newWindow = window.open(printUrl);
        console.log(printUrl); // Log the URL to the console
        // Additional logic if needed
      },
      __("Lang-Print")
    );
  },

  share_application_marathi_print(frm) {
    frm.add_custom_button(
      __("Marathi"),
      function () {
        var printUrl = frappe.urllib.get_full_url(
          "/api/method/frappe.utils.weasyprint.download_pdf?" +
            "doctype=" +
            encodeURIComponent("Share Application") +
            "&name=" +
            encodeURIComponent(frm.doc.name) +
            "&print_format=Share Marathi Form" +
            "&letterhead=Share Head Marathi"
        );
        var newWindow = window.open(printUrl);
        console.log(printUrl); // Log the URL to the console
        // Additional logic if needed
      },
      __("Lang-Print")
    );
  },

  share_application_default_print(frm) {
    frm.add_custom_button(__("Form Print"), function () {
      var printUrl = frappe.urllib.get_full_url(
        "/api/method/frappe.utils.weasyprint.download_pdf?" +
          "doctype=" +
          encodeURIComponent("Share Application") +
          "&name=" +
          encodeURIComponent(frm.doc.name) +
          "&print_format=Share Marathi Form" +
          "&letterhead=Share Head Marathi"
      );

      // Open a new window with specific window features to hide the address bar
      var newWindow = window.open(
        printUrl,
        "_blank",
        "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600"
      );

      console.log(printUrl); // Log the URL to the console
      // Additional logic if needed
    });
  },

  share_certificate_print(frm) {
    frm.add_custom_button(__("Certificate"), function () {
      if (frm.doc.application_sr_no_barcode) {
        console.log("barcode");
      } else {
        console.log("blank barcode");
      }
      frappe.call({
        method:
          "share_holder_management.share_holder_management.doctype.share_application.share_application.share_certificate_template",
        args: { docname: frm.doc.name },
        callback: function (response) {
          if (response.message && response.message.html_content) {
            var newWindow = window.open();
            newWindow.document.write(response.message.html_content);
          }
        },
      });
    });
  },

  custome_home_button(frm) {
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
  },
});
