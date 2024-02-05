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
                      body {
                          margin: 0; /* Remove default body margin */
                          padding: 0; /* Remove default body padding */
                      }
              
                      table {
                          border-collapse: collapse;
                          width: 100%;
                          margin-top: 20px;
                          overflow: hidden;
                      }
              
                      .branch-th {
                          background-color: #c2d7df;
                          height: 50px;
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
              
                      .branch-row_border {
                          border-bottom: 1px solid;
                          height: 60px;
                      }
              
                      .branch-row_border:hover {
                          background-color: yellow;
                          cursor: pointer;
                      }
              
                      .start-time {
                          color: green;
                          
                      }
              
                      .end-time {
                          color: red;
                      }
              
                      .branch_heading {
                          display: flex;
                          justify-content: space-between;
                          align-items: start;
                        
                      }
              
                     
              
                      label {
                        margin-right: 5px;
                        margin-bottom: 0;
                        font-weight: bold;
                        color: black;

                      }
              
                      select {
                          width: 150px;
                          padding: 5px; /* Add padding for styling */
                      }
                      #totalRows{
                        text-align:right;
                        
                      }
                  </style>
              </head>
              <body>
                  <div class="branch_heading">
                      <div class="heading_left">
                          <h3>Branch Log Information</h3>
                      </div>
                      <div class="heading_right">
                      <label for="branchSearch">Search:</label>
                      <input type="text" id="branchSearch" placeholder="Search by Branch">

                          <!-- Add the filter select dropdown -->
                          <label for="filter">Sort By:</label>
                          <select id="filter">
                              <option value="all">All</option>
                              <option value="started"> Started</option>
                              <option value="ended"> Ended </option>
                              <option value="notStarted">Not Started</option>
                              <option value="notEnded">Not Ended</option>
                          </select>
                      </div>
                  </div>
                  <!-- Show Total Row count -->
                  <div><h5 id="totalRows"></h5></div>
                  
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
                                                ? "<span class='start-time'>Started </span>"
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
                                                ? "<span class='end-time'>Ended </span>"
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
              </html>
              `;

              // Set the above `html` as Summary HTML
              frm.set_df_property("branch_log_html", "options", html);

              const filterDropdown = document.getElementById("filter");
              const branchSearchInput = document.getElementById("branchSearch");
              const branchSearchLabel = document.querySelector(
                'label[for="branchSearch"]'
              );
              const totalRowsElement = document.getElementById("totalRows");

              // Function to filter rows based on both filters
              function applyFilters() {
                const filterValue = filterDropdown.value;
                const searchValue = branchSearchInput.value
                  .trim()
                  .toLowerCase();

                const rows = document.querySelectorAll(".branch-row_border");
                let visibleRowIndex = 1;

                rows.forEach((row) => {
                  const started = row.querySelector(".start-time");
                  const ended = row.querySelector(".end-time");
                  const branch = row
                    .querySelector(".branch-td:nth-child(2)")
                    .textContent.toLowerCase();

                  const matchesFilter =
                    filterValue === "all" ||
                    (filterValue === "started" && started) ||
                    (filterValue === "ended" && ended) ||
                    (filterValue === "notStarted" && !started) ||
                    (filterValue === "notEnded" && !ended);

                  const matchesBranchSearch = branch.includes(searchValue);

                  if (matchesFilter && matchesBranchSearch) {
                    row.style.display = "";
                  } else {
                    row.style.display = "none";
                  }

                  // Update serial number only for visible rows
                  if (row.style.display !== "none") {
                    row.querySelector(".branch-td:first-child").textContent =
                      visibleRowIndex++;
                  }
                });

                // Update and display the total number of visible rows
                totalRowsElement.textContent = `Total records ${
                  visibleRowIndex - 1
                }`;
              }

              // Add event listener for filter changes
              filterDropdown.addEventListener("change", applyFilters);

              // Add event listener for branch search changes
              branchSearchInput.addEventListener("input", applyFilters);

              // Set initial styling for branch search label
              branchSearchLabel.style.marginRight = "5px";
              branchSearchLabel.style.fontWeight = "bold";
              branchSearchLabel.style.color = "black";
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
          console.log("Response", r.message);

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

              //start deatils response
              const startDetails = data.start_details || {};
              console.log("start details : ", startDetails);

              //end details response
              const endDetails = data.end_details || {};

              console.log("end details", endDetails);

              // total start branches response
              const totalStart = data.total_start_count;
              console.log("Total Number of start : ", totalStart);

              // total start branches response
              const totalEnd = data.total_end_count;
              console.log("Total Number of end : ", totalEnd);

              //total branches response
              const totalBranch = data.total_branch_count || {};
              console.log("Total Number of Branches : ", totalBranch);

              // Check if HO day is not started to display the start button
              const startButtonHtml = !startDetails.log_type
                ? `<button class="ho_button"  onclick="startHO()">Start HO Day</button>`
                : "";

              // Check if log_type is "Start" to set ho_day_start to true
              const hoDayStartLabel =
                startDetails.log_type === "Start"
                  ? `<span style="color: green;">HO Day Start</span>`
                  : `<span style="color: red;">HO Day Not Started Yet</span>`;

              const hoDayStartInfo =
                startDetails.log_type === "Start"
                  ? `${startDetails.ho_start_time} - ${startDetails.ho_start_date}`
                  : "";

              // Check if HO day is not ended to display the end button
              const endButtonHtml =
                totalEnd === totalBranch
                  ? `<button class="ho_button" onclick="startHO()">End HO Day</button>`
                  : "";

              // Check if log_type is "End" to set ho_day_end to true
              const hoDayEndLabel =
                endDetails.log_type === "End"
                  ? `<span style="color: green;">HO Day End</span>`
                  : `<span style="color: red;">HO Day Not Ended Yet</span>`;

              const hoDayEndInfo =
                endDetails.log_type === "End"
                  ? `${endDetails.ho_end_time} - ${endDetails.ho_end_date}`
                  : "";

              // Calculate the progress percentage based on the number of branches started
              const branchStartProgressPercentage =
                (totalStart / totalBranch) * 100;

              // Calculate the progress percentage based on the number of branches ended
              const branchEndProgressPercentage =
                (totalEnd / totalBranch) * 100;

              // Generate HTML dynamically based on the fetched data
              let html = `<!DOCTYPE html>
          <html lang="en">
            <head>
              <meta charset="UTF-8" />
              <meta name="viewport" content="width=device-width, initial-scale=1.0" />
              <title>Share Application Day Management </title>
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
                  text-align: center;
                  border-radius: 15px;
                }
          
                .ho_label {
                  font-size: 16px;
                  font-weight: bold;
                  margin-bottom: 5px;
                }
          
                .ho_value {
                  align-items: center;
                  color: green;
                }
          
                .ho_delta,
                .ho_label-secondary {
                  font-size: 12px;
                  color: #ccc;
                  
                }
          
                .ho_metric-grid {
                  display: flex;
                  justify-content: space-between;
                }
                .ho_progress-container {
                  display: flex;
                  align-items: center;
                  width: 100%;
                  height: 14px;
                  background-color: #D9D9D9;
                  border-radius: 20px;
                  overflow: hidden; /* Hide overflow to round the corners */
                }

                .ho_progress-bar {
                  height: 100%;
                  background-color: #50c878; /* Green color */
                  border-radius: 20px;
                  transition: width 0.3s ease; /* Add transition for smooth width changes */
                }

          
                /* Button style */
                .ho_button {
                  background-color: #4caf50;
                  border: none;
                  color: white;
                  padding: 8px 20px;
                  text-align: center;
                  text-decoration: none;
                  display: inline-block;
                  font-size: 16px;
                  cursor: pointer;
                  border-radius: 21px;
                  margin-top: 15px;
                }
          
                button.ho_button:focus {
                  outline: none !important;
                }
              </style>
              <script>
                // Function to start the HO Day
                function startHO() {
                  // Redirect to another page (replace 'YOUR_URL' with the actual URL)
                  // route in parts
                  frappe.new_doc("Day Management Checkin", function (doc) {
                    frappe.set_route("Form", "Day Management Checkin", doc.name);
                  });
                }
              </script>
            </head>
          
            <body>
            
              <div class="ho_container">
              
                <div class="ho_header">
                  <div class="ho_title">Share Application Day Management ${formattedDate}</div>
                  <div class="ho_mql">Developed by - Talib Sheikh</div>
                </div>
                <div class="ho_metrics">
                  <div class="ho_metric">
                    <div class="ho_label">${hoDayStartLabel}</div>
                    <div class="ho_value">${hoDayStartInfo}</div>
                    <!-- Display the start button HTML conditionally -->
                    ${startButtonHtml}
                  </div>
                  <div class="ho_metric">
                    <div class="ho_label">${hoDayEndLabel}</div>
                    <div class="ho_value">${hoDayEndInfo}</div>
                    <!-- Display the End button HTML conditionally -->
                    ${endButtonHtml}
                  </div>
                  <div class="ho_metric">
                    <div class="ho_metric-grid">
                      <div class="ho_label">Branch Day Start</div>
                      <div class="ho_value">
                      <span
                          style="color: #948C8C;  font-size: 14px; font-weight: 600;"
                          class="ho_label-secondary"
                          >BRANCHES</span
                        >
                        <span class="ho_value-text" style="font-size: 14px;"
                          >${
                            totalStart > 0
                              ? String(totalStart).padStart(2, "0")
                              : totalStart
                          }/${String(totalBranch).padStart(2, "0")}</span
                        >
                        
                      </div>
                    </div>
          
                    <br />
                    <div class="ho_progress-container">
                      <div
                        class="ho_progress-bar"
                        style="width: ${branchStartProgressPercentage}%;"
                      ></div>
                    </div>
                  </div>
                  <div class="ho_metric">
                  <div class="ho_metric-grid">
                    <div class="ho_label">Branch Day End</div>
                    <div class="ho_value">
                    <span
                          style="color: #948C8C;  font-size: 14px; font-weight: 600;"
                          class="ho_label-secondary"
                          >BRANCHES</span
                        >
                      <span class="ho_value-text" style="font-size: 14px;"
                        >${
                          totalEnd > 0
                            ? String(totalEnd).padStart(2, "0")
                            : totalEnd
                        }/${String(totalBranch).padStart(2, "0")}</span
                      >
          
                    </div>
                    </div>
                    <br />
                    <div class="ho_progress-container">
                      <div
                        class="ho_progress-bar"
                        style="width: ${branchEndProgressPercentage}%;"
                      ></div>
                    </div>
                  </div>
                  <!-- Add more metrics here -->
                </div>
              </div>
            </body>
          </html>
          `;

              // Set the above `html` as Summary HTML
              frm.set_df_property("ho_log_html", "options", html);
            },
          });
        } else {
          frappe.msgprint("Error fetching details");
        }
      },
    });
  },
});
