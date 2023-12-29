// Copyright (c) 2023, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Application", {
  refresh(frm) {
    if (frm.is_new()) {
      frm.call({
        method: "check_last_application_sr_no",
        args: {},
        callback: function (r) {
          // Check if the message array contains at least one object
          if (r.message) {
            // Log the response value to the console
            console.log("Response -----");
            console.log("Response:", r.message);

            frm.set_value("application_sr_no", r.message);
            frm.refresh_field("application_sr_no");

            // Do something else with the response, if needed
          } else {
            frappe.throw("Server Down . .");
            // Handle the case where there is no response
          }
        },
      });
    }

    // frm.trigger("set_base_share_amount");
    frm.trigger("set_share_application_amount");

    //when form submitted, the form will be locked it means not editable;
    if (frm.doc.status == "Submitted") {
      frm.trigger("set_form_lock");
    }
  },

  no_of_shares(frm) {},
  onload_post_render: function (frm) {
    let share_base_amount = 100;

    frm.fields_dict["no_of_shares"].$input.on("input", function (event) {
      var value = frm.fields_dict["no_of_shares"].get_value();
      console.log("Real-time input. No. of shares: ", value);

      // Perform the calculation
      var noOfShares = value || 0;
      var baseShareAmount = share_base_amount || 0;
      var applicationCharges = frm.doc.share_application_charges || 0;
      var totalAmount = noOfShares * baseShareAmount + applicationCharges;
      var total_base_amount = noOfShares * baseShareAmount;
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
      frm.set_value("base_share_amount", total_base_amount);
      frm.refresh_field("base_share_amount");

      // Set the calculated total amount back to the form
      frm.set_value("tot_share_amt", totalAmount);
      frm.refresh_field("tot_share_amt");

      // Log the calculated total amount to the console
      console.log("Calculated Total Amount: ", totalAmount);
    });

    // Trigger the initial calculation
    //frm.trigger('calculate_total_amount');
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
