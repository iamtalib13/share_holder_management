// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Share Amount Setting", {
  refresh: function (frm) {
    frm.disable_save();
    frm.fields_dict.add_share_amount.$input.css({
      "background-color": "black", // Set the background color to black
      color: "white", // Set the text color to white
      width: "100%", // Set width to 100%
      position: "relative", // Add position: relative
      padding: "10px", // Add padding for better visibility and aesthetics
      border: "none", // Remove border if needed
      cursor: "pointer", // Change cursor to pointer for better UX
    });
    frm.fields_dict["share_amount_details"].grid.wrapper
      .find(".grid-add-row")
      .hide();
  },
  add_share_amount: function (frm) {
    let amount = frm.doc.amount;
    let date = frm.doc.date;

    if (!amount) {
      frappe.throw("Please fill Amount");
    } else if (!date) {
      frappe.throw("Please fill Date");
    } else {
      let row = frm.add_child("share_amount_details", {
        amount: amount,
        date: date,
      });

      frm.refresh_field("share_amount_details");

      frm.set_value("amount", null);
      frm.set_value("date", null);

      frm.save();
    }
  },

  save_status: function (frm) {
    for (let row of frm.doc.share_amount_details) {
      if (row.status == "Enable") {
        let amount = row.amount;
        frm.set_value("current_amount", amount);
        frm.refresh_field("current_amount");
        console.log("Current price :", amount);
      }
    }
    frm.save();
  },
});
