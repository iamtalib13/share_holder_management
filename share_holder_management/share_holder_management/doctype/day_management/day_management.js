// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Day Management", {
  refresh: function (frm) {
    frm.trigger("populate_ho_log_html");
    frm.trigger("populate_branch_log_html");

    //frm.trigger("day_intro");
    if (!frm.doc.day_start) {
      // frm
      //   .add_custom_button(__("Day Start"), function () {
      //     frappe.confirm(
      //       "Are you sure ?",
      //       () => {
      //         frm.call({
      //           method: "get_server_datetime",
      //           callback: function (r) {
      //             if (!r.exc && r.message) {
      //               frm.set_value("day_start", r.message);
      //               frm.refresh_field("day_start");
      //               frm.save();
      //             } else {
      //               // Handle the case where there is an error or no response
      //               console.error(
      //                 "SERVER INTERNET ERROR ",
      //                 r.exc || "No response"
      //               );
      //             }
      //           },
      //         });
      //       },
      //       () => {
      //         // action to perform if No is selected
      //       }
      //     );
      //   })
      //   .css({
      //     "background-color": "#28a745", // Set green color
      //     color: "#ffffff", // Set font color to white
      //   });
    }

    if (!frm.doc.day_end) {
      // frm
      //   .add_custom_button(__("Day End"), function () {
      //     frappe.confirm(
      //       "Are you sure ?",
      //       () => {
      //         frm.call({
      //           method: "get_server_datetime",
      //           callback: function (r) {
      //             if (!r.exc && r.message) {
      //               frm.set_value("day_end", r.message);
      //               frm.refresh_field("day_end");
      //               frm.save();
      //             } else {
      //               // Handle the case where there is an error or no response
      //               console.error(
      //                 "SERVER INTERNET ERROR ",
      //                 r.exc || "No response"
      //               );
      //             }
      //           },
      //         });
      //       },
      //       () => {
      //         // action to perform if No is selected
      //       }
      //     );
      //   })
      //   .css({
      //     "background-color": "#28a745", // Set green color
      //     color: "#ffffff", // Set font color to white
      //   });
    }
  },

  day_intro: function (frm) {
    frm.set_intro("<b>Day Start : </b>" + frm.doc.day_start, "green");
    frm.set_intro("<b>Day End : </b>" + frm.doc.day_end, "green");
  },

  async populate_branch_log_html(frm) {
    // Fetch the data from the backend (check above for sample response)
    frm.call({
      method: "show_branch_logs",
      args: {
        self: frm.doc.name,
      },
      callback: function (r) {
        if (!r.exc) {
          const data = r.message;
          console.log(data);

          // Generate HTML directly in JavaScript
          let html = `
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Branch Log Information</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif; /* Use a common font */
                            }

                            table {
                                border-collapse: collapse;
                                width: 100%;
                                margin-top: 20px;
                                overflow: hidden; /* Hide the vertical scrollbar */
                            }
                            th {
                              background-color: #c2d7df;
                          }
                            

                            th, td {
                                border: none;
                                padding: 8px;
                                text-align: left;
                            }

                            thead {
                                position: sticky;
                                top: 0;
                                z-index: 100;
                            }

                            tbody tr:hover {
                                background-color: yellow;
                                cursor: pointer;
                            }
                        </style>
                    </head>
                    <body>
                        <h3>Branch Log Information</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Sr. No.</th>
                                    <th>Branch</th>
                                    <th>Start Date and Time</th>
                                    <th>Day Start By</th>
                                    <th>End Date and Time</th>
                                    <th>Day End By</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.result
                                  .map(
                                    (row, index) => `
                                            <tr class="row_custom_border">
                                                <td>${index + 1}</td>
                                                <td>${row.branch}</td>
                                                <td>${
                                                  row.start_time
                                                    ? `${
                                                        row.start_log_type
                                                          ? "<span style='color:green; font-weight: 600;'>Start on </span>"
                                                          : ""
                                                      }<br>${new Date(
                                                        row.start_time
                                                      ).toLocaleString(
                                                        "en-GB",
                                                        {
                                                          day: "numeric",
                                                          month: "numeric",
                                                          year: "numeric",
                                                          hour: "2-digit",
                                                          minute: "2-digit",
                                                          hour12: true,
                                                        }
                                                      )}`
                                                    : ""
                                                }</td>
                                                <td>${
                                                  row.Day_Start_by || ""
                                                }</td>
                                                <td>${
                                                  row.end_time
                                                    ? `${
                                                        row.end_log_type
                                                          ? "<span style='color:red; font-weight: 600;'>End on </span>"
                                                          : ""
                                                      }<br>${new Date(
                                                        row.end_time
                                                      ).toLocaleString(
                                                        "en-GB",
                                                        {
                                                          day: "numeric",
                                                          month: "numeric",
                                                          year: "numeric",
                                                          hour: "2-digit",
                                                          minute: "2-digit",
                                                          hour12: true,
                                                        }
                                                      )}`
                                                    : ""
                                                }</td>
                                                <td>${
                                                  row.Day_End_by || " "
                                                }</td>
                                            </tr>
                                        `
                                  )
                                  .join("")}
                            </tbody>
                        </table>
                    </body>
                    </html>
                `;

          // Set the above `html` as Summary HTML
          frm.set_df_property("branch_log_html", "options", html);
        } else {
          frappe.msgprint("Error fetching details");
        }
      },
    });
  },

  async populate_ho_log_html(frm) {
    // Fetch the data from backend (check above for sample response)
    frm.call({
      method: "show_ho_logs",
      args: {
        self: frm.doc.name,
      },
      callback: function (r) {
        if (!r.exc) {
          const data = r.message;
          console.log(data);

          // Generate HTML directly in JavaScript with formatted date and time
          let html = `
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Branch Log Information</title>
                        <style>
                        .main {
                          text-align: center;
                          background-color: #f0f0f0;

                      }
                        .container_ho {
                          display: inline-flex;
                          gap: 20px;
                          justify-content: space-between;
                          /* Additional styling for demonstration purposes */
                          background-color: #f0f0f0;
                          padding: 20px;
                      }
              
                      .card {
                          width: 150px;
                          height: 200px;
                          border: 1px solid #ccc;
                          border-radius: 8px;
                          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                      }
                        </style>
                    </head>
                    <body>
                        <h3>Head Office</h3>
                        <div class="main">
                    <div class="container_ho">
                        <div class="card">
                        card111 for day start
                        </div>
                        <div class="card">
                        card111 for day end

                        </div>
                    </div>
                      </div>
                    </body>
                    </html>
                `;

          // Set the above `html` as Summary HTML
          frm.set_df_property("ho_log_html", "options", html);
        } else {
          frappe.msgprint("Error fetching details");
        }
      },
    });
  },
});
