frappe.ui.form.on("Day Management Checkin", {
  // onload: function (frm) {
  //   if (frm.is_new()) {
  //     setTimeout(function () {
  //       cur_frm.refresh();
  //       frm.set_value("refresh", "true");
  //     }, 2000); // 2000 milliseconds = 2 seconds
  //   }
  // },

  refresh: function (frm) {
    if (frm.is_new()) {
      // Logic for new form
      // if (frm.doc.refresh == "false") {
      //   setTimeout(function () {
      //     cur_frm.refresh();
      //     frm.set_value("refresh", "true");
      //   }, 2000); // 2000 milliseconds = 2 seconds
      // }

      let user = frappe.session.user;
      let eidMatch = user.match(/\d+/);
      let eid = eidMatch ? eidMatch[0] : "";

      let modifiedEmployeeId = "";
      if (user.includes("ABPS")) {
        modifiedEmployeeId = "ABPS" + eid;
      } else if (user.includes("MCPS")) {
        modifiedEmployeeId = "MCPS" + eid;
      } else {
        modifiedEmployeeId = eid;
      }
      frm.set_value("employee", modifiedEmployeeId);

      frappe.db.get_value(
        "Employee",
        { employee: frm.doc.employee },
        "branch",
        function (response) {
          if (response && response.branch) {
            let branch = response.branch;
            frm.set_value("branch", response.branch);

            if (branch == "Gondia HO") {
              // Logic for Gondia HO
              frm.call({
                method: "ho_day_start_and_end",
                args: { branch: branch },
                callback: function (r) {
                  if (!r.exc) {
                    if (r.message === "Day Completed") {
                      frm.set_df_property("log_type", "options", "");
                      frm.disable_save();
                      frm.disable_form();
                    } else if (r.message === "Day Not Ended") {
                      frm.set_df_property("log_type", "options", "End");
                    } else if (r.message === "Day Not Started") {
                      frm.set_df_property("log_type", "options", "Start");
                    }
                  } else {
                    console.log("Error:", r.exc);
                  }
                },
              });
            } else {
              // Logic for other branches
              frm.call({
                method: "get_branch_checkin_details",
                args: { branch: branch },
                callback: function (r) {
                  if (!r.exc) {
                    // Handle branch-specific responses
                  } else {
                    console.log("Error:", r.exc);
                  }
                },
              });

              frm.call({
                method: "branch_day_start_and_end",
                args: { branch: branch },
                callback: function (r) {
                  if (!r.exc) {
                    if (r.message === "Day Completed") {
                      frm.set_df_property("log_type", "options", "");
                      frm.disable_save();
                      frm.disable_form();
                    } else if (r.message === "Day Not Ended") {
                      frm.set_df_property("log_type", "options", "End");
                    } else if (r.message === "Day Not Started") {
                      frm.set_df_property("log_type", "options", "Start");
                    }
                  } else {
                    console.log("Error:", r.exc);
                  }
                },
              });
            }
          }
        }
      );
    } else if (!frm.is_new()) {
      // Logic for existing forms
    }
  },

  after_save: function (frm) {
    if (frappe.user.has_role("Share Executive")) {
      frappe.set_route("/app/day-management");
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
                "You cannot End HO until branches are not ended for today."
              );
              frm.set_value("log_type", "");
            }
          }
        },
      });
    }
  },
});
frappe.ui.form.on("Day Management Checkin", "onload", function (frm) {
  frm.refresh();
});
