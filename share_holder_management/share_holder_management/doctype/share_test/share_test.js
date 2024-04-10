frappe.ui.form.on("Share Test", {
  refresh: function (frm) {
    frm.add_custom_button(__("Send Data"), function () {
      // Trigger the 'send_data' method
      let first_name = frm.doc.first_name;
      let last_name = frm.doc.last_name;

      frm.call({
        method: "send_data",
        args: {
          first_name: first_name,
          last_name: last_name,
        },
        callback: function (r) {
          if (!r.exc) {
            if (r.message && r.message.success) {
              frappe.msgprint(r.message.message);
            } else {
              frappe.msgprint("Data submission failed");
            }
          }
        },
      });
    });

    frm.add_custom_button(__("get products"), function () {
      frm.call({
        method: "receive_data",
        callback: function (r) {
          if (!r.exc) {
            frappe.msgprint("Data submitted successfully");
          }
        },
      });
    });
    frm.add_custom_button(__("get xml"), function () {
      frm.call({
        method: "receive_xml_data",
        callback: function (r) {
          if (!r.exc) {
            frappe.msgprint("Data submitted successfully");
          }
        },
      });
    });
  },
});
