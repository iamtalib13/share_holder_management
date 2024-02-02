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
          frm.call({
            method: "get_server_datetime",
            callback: function (r) {
              const serverDateTime = r.message;
              console.log(serverDateTime);

              // Convert the server datetime to a JavaScript Date object
              const dateObject = new Date(serverDateTime);

              // Extract individual components (year, month, day)
              const year = dateObject.getFullYear();
              const month = (dateObject.getMonth() + 1)
                .toString()
                .padStart(2, "0"); // Months are zero-based
              const day = dateObject.getDate().toString().padStart(2, "0");

              // Form the desired date string
              const formattedDate = `${day}-${month}-${year}`;

              // Generate HTML directly in JavaScript
              let html = `<html lang="en">
              <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Branch Log Information</title>
                  <style>
                      body {}
                      table {
                          border-collapse: collapse;
                          width: 100%;
                          margin-top: 20px;
                          overflow: hidden;
                      }
                      .branch-th {
                          background-color: #c2d7df;
                          height: 40px;
                          text-align: center;
                      }
                      .branch-td {
                          border: none;
                          padding: 8px;
                          text-align: center;
                      }
                      thead {
                          position: sticky;
                          top: 0;
                          z-index: 100;
                      }
                      .branch-row_border:hover {
                          background-color: yellow;
                          cursor: pointer;
                      }
                      .start-time { color: green; }
                      .end-time { color: red; }
                  </style>
              </head>
              <body>
                  <h3>Branch Log Information - ${formattedDate}</h3>
                  <table class="branch_log_html_table">
                      <thead>
                          <tr>
                              <th class="branch-th">Sr. No.</th>
                              <th class="branch-th">Branch</th>
                              <th class="branch-th">Start Date and Time</th>
                              <th class="branch-th">Day Start By</th>
                              <th class="branch-th">End Date and Time</th>
                              <th class="branch-th">Day End By</th>
                          </tr>
                      </thead>
                      <tbody>
                          ${data.result
                            .map(
                              (row, index) => `<tr class="branch-row_border">
                                      <td class="branch-td">${index + 1}</td>
                                      <td class="branch-td">${row.branch}</td>
                                      <td class="branch-td">${
                                        row.start_time
                                          ? `${
                                              row.start_log_type
                                                ? "<span class='start-time'>Start on </span>"
                                                : ""
                                            }<br>${new Date(
                                              row.start_time
                                            ).toLocaleString("en-GB", {
                                              day: "numeric",
                                              month: "numeric",
                                              year: "numeric",
                                              hour: "2-digit",
                                              minute: "2-digit",
                                              hour12: true,
                                            })}`
                                          : ""
                                      }</td>
                                      <td class="branch-td">${
                                        row.Day_Start_by || ""
                                      }</td>
                                      <td class="branch-td">${
                                        row.end_time
                                          ? `${
                                              row.end_log_type
                                                ? "<span class='end-time'>End on </span>"
                                                : ""
                                            }<br>${new Date(
                                              row.end_time
                                            ).toLocaleString("en-GB", {
                                              day: "numeric",
                                              month: "numeric",
                                              year: "numeric",
                                              hour: "2-digit",
                                              minute: "2-digit",
                                              hour12: true,
                                            })}`
                                          : ""
                                      }</td>
                                      <td class="branch-td">${
                                        row.Day_End_by || " "
                                      }</td>
                                  </tr>`
                            )
                            .join("")}
                      </tbody>
                  </table>
              </body>
              </html>`;

              // Set the above `html` as Summary HTML
              frm.set_df_property("branch_log_html", "options", html);
            },
          });
        } else {
          frappe.msgprint("Error fetching details");
        }
      },
    });
  },

  async populate_ho_log_html(frm) {
    // Fetch the data from backend
    frm.call({
      method: "show_ho_logs",
      args: {
        self: frm.doc.name,
      },
      callback: function (r) {
        if (!r.exc) {
          const data = r.message;
          console.log(data);

          // // Check if log_type is "Start" to set ho_day_start to true
          // const hoDayStartLabel =
          //   data.log_type === "Start"
          //     ? "HO Day Start"
          //     : "HO Day Not Started Yet";
          // const hoDayStartInfo =
          //   data.log_type === "Start"
          //     ? `${data.ho_start_time} - ${data.ho_start_date}`
          //     : "HO Day Not Started Yet";

          // Check if log_type is "Start" to set ho_day_start to true
          const hoDayStartLabel =
            data.log_type === "Start"
              ? "HO Day Start"
              : "HO Day Not Started Yet";
          const hoDayStartInfo =
            data.log_type === "Start"
              ? `${data.ho_start_time} - ${data.ho_start_date}`
              : "HO Day Not Started Yet";

          // Check if HO day is not started to display the start button
          const startButtonHtml = !data.log_type
            ? `<button onclick="startHO()">Start HO Day</button>`
            : "";

          // Generate HTML dynamically based on the fetched data
          let html = `<!DOCTYPE html>
                        <html lang="en">
                        
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Share Application Day Management</title>
                            <style>
                                body {
                                    font-family: sans-serif;
                                    margin: 0;
                                    padding: 20px;
                                }
                        
                                .ho_container {
                                    background-color: #f5f5f5;
                                    border-radius: 5px;
                                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                                    padding: 20px;
                                }
                        
                                .ho_header {
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 20px;
                                }
                        
                                .ho_title {
                                    font-size: 20px;
                                    font-weight: bold;
                                }
                        
                                .ho_mql {
                                    color: #ccc;
                                    font-size: 14px;
                                }
                        
                                .ho_metrics {
                                    display: grid;
                                    grid-template-columns: repeat(2, 1fr);
                                    gap: 20px;
                                }
                        
                                .ho_metric {
                                    background-color: #fff;
                                    border-radius: 5px;
                                    padding: 15px;
                                }
                        
                                .ho_label {
                                    font-size: 16px;
                                    font-weight: bold;
                                    margin-bottom: 5px;
                                }
                        
                                .ho_value {
                                    display: flex;
                                    align-items: center;
                                }
                        
                                .ho_delta,
                                .ho_label-secondary {
                                    font-size: 12px;
                                    color: #ccc;
                                    margin-left: 5px;
                                }
                        
                                /* Progress bars */
                                .ho_progress-container {
                                    display: flex;
                                    align-items: center;
                                    width: 100%;
                                    height: 8px;
                                    background-color: #ddd;
                                    border-radius: 4px;
                                }
                        
                                .ho_progress-bar {
                                    height: 100%;
                                    background-color: #50C878; /* Green color */
                                    border-radius: 4px;
                                }
                            </style>
                            <script>
                            function startHO() {
                                if (confirm('Are you sure you want to start HO Day?')) {
                                    frappe.ui.form.on('Day Management', 'refresh', function (frm) {
                                        frm.trigger('start_ho_day');
                                        frappe.set_route("List", "Day Management");
                                    });
                                }
                            }
                        </script>
                        </head>
                        
                        <body>
                            <div class="ho_container">
                                <div class="ho_header">
                                    <div class="ho_title">Share Application Day Management</div>
                                    <div class="ho_mql">Developed by - Talib Sheikh</div>
                                </div>
                                <div class="ho_metrics">
                                <div class="ho_metric">
                                <div class="ho_label">${hoDayStartLabel}</div>
                                <div class="ho_value">
                                    ${hoDayStartInfo}
                                </div>
                            </div>
                                    <div class="ho_metric">
                                        <div class="ho_label">HO Day End</div>
                                        <div class="ho_value">
                                            ${
                                              data.ho_day_end
                                                ? `${data.ho_end_time} - ${data.ho_end_date}`
                                                : "HO Day Not Ended Yet"
                                            }
                                        </div>
                                    </div>
                                    <div class="ho_metric">
                                        <div class="ho_label">Branch Day Start</div>
                                        <div class="ho_value">
                                            <span class="ho_value-text">${
                                              data.branch_start
                                            }/${data.total_branch}</span>
                                            <span style="color: #50C878; font-size:15px;" class="ho_label-secondary">Total Branch</span>
                                        </div>
                                        <br>
                                        <div class="ho_progress-container">
                                            <div class="ho_progress-bar" style="width: ${
                                              (data.branch_start /
                                                data.total_branch) *
                                              100
                                            }%;"></div>
                                        </div>
                                    </div>
                                    <div class="ho_metric">
                                        <div class="ho_label">Branch Day End</div>
                                        <div class="ho_value">
                                            <span class="ho_value-text">${
                                              data.branch_end
                                            }/${data.total_branch}</span>
                                            <span style="color: #50C878; font-size:15px;" class="ho_label-secondary">Total Branch</span>
                                        </div>
                                        <br>
                                        <div class="ho_progress-container">
                                            <div class="ho_progress-bar" style="width: ${
                                              (data.branch_end /
                                                data.total_branch) *
                                              100
                                            }%;"></div>
                                        </div>
                                    </div>
                                    <!-- Add more metrics here -->
                                </div>
                            </div>
                        </body>
                        
                        </html>`;

          // Set the above `html` as Summary HTML
          frm.set_df_property("ho_log_html", "options", html);
        } else {
          frappe.msgprint("Error fetching details");
        }
      },
    });
  },
});

// // Function to start the HO Day
// function startHO() {
//   // Redirect to another page (replace 'YOUR_URL' with the actual URL)
//   window.location.href = "";
// }
