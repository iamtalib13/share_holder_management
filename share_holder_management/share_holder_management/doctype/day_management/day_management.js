// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Day Management", {
  refresh: function (frm) {
    frm.fields_dict["schedule_table"].grid.wrapper.find(".grid-add-row").hide();
    frm.trigger("day_intro");
    if (!frm.doc.day_start) {
      frm
        .add_custom_button(__("Day Start"), function () {
          frappe.confirm(
            "Are you sure ?",
            () => {
              frm.call({
                method: "get_server_datetime",
                callback: function (r) {
                  if (!r.exc && r.message) {
                    frm.set_value("day_start", r.message);
                    frm.refresh_field("day_start");

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
    }

    if (!frm.doc.day_end) {
      frm
        .add_custom_button(__("Day End"), function () {
          frappe.confirm(
            "Are you sure ?",
            () => {
              frm.call({
                method: "get_server_datetime",
                callback: function (r) {
                  if (!r.exc && r.message) {
                    frm.set_value("day_end", r.message);
                    frm.refresh_field("day_end");

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
    }
  },

  day_intro: function (frm) {
    frm.set_intro("<b>Day Start : </b>" + frm.doc.day_start, "green");
    frm.set_intro("<b>Day End : </b>" + frm.doc.day_end, "green");
  },
});
