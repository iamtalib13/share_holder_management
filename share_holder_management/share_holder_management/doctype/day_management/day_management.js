// Copyright (c) 2024, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Day Management", {
  refresh: function (frm) {
    frm.trigger("header_links");
    frm.trigger("populate_ho_log_html");
    frm.trigger("day_management_status");
    // frm.trigger("populate_branch_log_html");
  },

  async day_management_status(frm) {
    // Make an asynchronous call to the Python function to fetch data
    frm.call({
      method: "check_conditions",
      callback: function (data) {
        // Log the response in the console
        console.log("status response:", data);

        // Handle the data received from the Python function
        let results = data.message;

        // Assuming results[0].Date is a valid date string
        const originalDate = new Date(results[0].Date);
        console.log("original date:", originalDate);

        // Extract day, month, and year
        const day = originalDate.getDate().toString().padStart(2, "0");
        const month = (originalDate.getMonth() + 1).toString().padStart(2, "0"); // Months are zero-based
        const year = originalDate.getFullYear();

        // Format the date as dd-mm-yyyy
        const formattedDate = `${day}-${month}-${year}`;

        console.log("Formatted Date:", formattedDate);

        // Generate HTML dynamically based on the fetched data
        let html = `<!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <title>Share Application Day Management </title>
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
                          height: 60px;
                          text-align: center;
                          font-size: 15px;
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
                          border-bottom: 1px solid #D9D9D9;
                          height: 60px;
                      }

                      .branch-row_border:hover {
                          background-color: #c2d7df;
                          cursor: pointer;
                      }

                      /* Add custom styles for the true and false symbols */
                      .checkmark {
                          color: green; /* Change color for true symbol */
                          font-size: x-large;
                      }
                    
                      .crossmark {
                          color: red; /* Change color for false symbol */
                          font-size: x-large;
                      }

                      </style>
                    </head>

                    <body>
                        <h3>Day Management Status</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th class="branch-th">Status</th>
                                    <th class="branch-th">Date</th>
                                    <th class="branch-th">HO Day Start</th>
                                    <th class="branch-th">All Branch Day Start</th>
                                    <th class="branch-th">All Branch Day End</th>
                                    <th class="branch-th">HO Day End</th>
                                </tr>
                            </thead>
                            <tbody>
                            ${results
                              .map(
                                (result) => `
                                <tr>
                                <td class="branch-td">${result.Status}</td>
                                <td class="branch-td">${formattedDate}</td>
                                <td class="branch-td ${
                                  result["HO Day Start"]
                                    ? "checkmark"
                                    : "crossmark"
                                }">
                                    ${
                                      result["HO Day Start"]
                                        ? "&#10004;"
                                        : "&#10008;"
                                    }
                                </td>
                                <td class="branch-td ${
                                  result["All Branch Day Start"]
                                    ? "checkmark"
                                    : "crossmark"
                                }">
                                    ${
                                      result["All Branch Day Start"]
                                        ? "&#10004;"
                                        : "&#10008;"
                                    }
                                </td>
                                <td class="branch-td ${
                                  result["All Branch Day End"]
                                    ? "checkmark"
                                    : "crossmark"
                                }">
                                    ${
                                      result["All Branch Day End"]
                                        ? "&#10004;"
                                        : "&#10008;"
                                    }
                                </td>
                                <td class="branch-td ${
                                  result["HO Day End"]
                                    ? "checkmark"
                                    : "crossmark"
                                }">
                                    ${
                                      result["HO Day End"]
                                        ? "&#10004;"
                                        : "&#10008;"
                                    }
                                </td>
                              </tr>
                            `
                              )
                              .join("")}
                        </tbody>
                        </table>
                    </body>
                </html>`;

        // Set the above `html` as Summary HTML
        frm.set_df_property("day_management_status", "options", html);
      },
    });
  },

  day_intro: function (frm) {
    frm.set_intro("<b>Day Start : </b>" + frm.doc.day_start, "green");
    frm.set_intro("<b>Day End : </b>" + frm.doc.day_end, "green");
  },
  async header_links(frm) {
    // Customize the navbar
    // Intercept the click event for "Share Management" link
    $("#navbar-breadcrumbs a[href='/app/share-management']").on(
      "click",
      function (event) {
        // Redirect to the home page
        window.location.href = "/app";
        event.preventDefault();
      }
    );
    $("#navbar-breadcrumbs a[href='/app/Executive']").on(
      "click",
      function (event) {
        // Redirect to the home page
        window.location.href = "/app";
        event.preventDefault();
      }
    );
  },

  //Showing HO logs details as html
  async populate_ho_log_html(frm) {
    // checking previous data record first
    frm.call({
      method: "check_conditions",
      freeze: true, // Set to true to freeze the UI
      freeze_message: "Please wait, processing data...",
      callback: function (r) {
        if (!r.exc) {
          const data = r.message;
          console.log("Response", r.message);
          console.log("data", data);

          // Assuming results[0].Date is a valid date string
          const currentDate = new Date(data[0].Date);
          console.log("original date:", currentDate);

          // Extract day, month, and year
          const day = currentDate.getDate().toString().padStart(2, "0");
          const month = (currentDate.getMonth() + 1)
            .toString()
            .padStart(2, "0"); // Months are zero-based
          const year = currentDate.getFullYear();

          // Format the date as dd-mm-yyyy
          const formattedDate = `${year}-${month}-${day}`;

          // Format the date as dd-mm-yyyy
          const showDate = `${day}-${month}-${year}`;

          // getting ho log records of passing date
          frm.call({
            method: "show_ho_logs",
            freeze: true, // Set to true to freeze the UI
            freeze_message: "Please wait, processing data...",
            args: {
              self: frm.doc.name,
              date: formattedDate, // Pass the formatted date to show_ho_logs
            },
            callback: function (r) {
              if (!r.exc) {
                const data = r.message;
                console.log("Response", r.message);

                // // Check if HO day is ended
                // const hoDayEnded = totalEnd === totalBranch;

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
                    ? `<span style="color: green;">HO Day Started</span>`
                    : `<span style="color: red;">HO Day Not Started Yet</span>`;

                const hoDayStartInfo =
                  startDetails.log_type === "Start"
                    ? `${startDetails.ho_start_time} - ${startDetails.ho_start_date}`
                    : "";

                // Check if end details is not present and all branches have ended to decide whether to show the "End HO Day" button
                const showEndButton =
                  !endDetails.log_type && totalEnd === totalBranch;

                // Display the "End HO Day" button only if end details are not present and all branches have ended
                const endButtonHtml = showEndButton
                  ? `<button class="ho_button" onclick="startHO()">End HO Day</button>`
                  : "";

                // Check if log_type is "End" to set ho_day_end to true
                const hoDayEndLabel =
                  endDetails.log_type === "End"
                    ? `<span style="color: green;">HO Day Ended</span>`
                    : `<span style="color: red;">HO Day will end when all branches day Ended</span>`;

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

                // Check if the HO day has ended
                const checkhoDayEnded = totalEnd === totalBranch;

                // Set the flag based on the condition
                const dayEndedFlag = checkhoDayEnded ? "true" : "false";
                console.log("Branch ended", dayEndedFlag);

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
                      <div class="ho_title">Share Application Day Management ${showDate}</div>
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

                // Check if HO day is started before triggering the branch log function
                if (startDetails.log_type === "Start") {
                  frm.trigger("populate_branch_log_html");
                }
              } else {
                frappe.msgprint("Error fetching details");
              }
            },
          });
        }
      },
    });
  },

  //Showing Branch logs details as html
  async populate_branch_log_html(frm) {
    // Fetch the data from the backend
    // checking previous data record first
    frm.call({
      method: "check_conditions",
      freeze: true, // Set to true to freeze the UI
      freeze_message: "Please wait, processing data...",
      callback: function (r) {
        if (!r.exc) {
          const data = r.message;
          console.log("Response", r.message);
          console.log("data", data);

          const currentDate = new Date(data[0].Date);
          console.log("original date:", currentDate);

          // Extract day, month, and year
          const day = currentDate.getDate().toString().padStart(2, "0");
          const month = (currentDate.getMonth() + 1)
            .toString()
            .padStart(2, "0"); // Months are zero-based
          const year = currentDate.getFullYear();

          const formatcurrentDate = `${year}-${month}-${day}`;
          console.log("formatcurrentDate", formatcurrentDate);

          const formattedDate = currentDate.toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          });

          const formattedTime = currentDate.toLocaleTimeString("en-GB", {
            hour: "2-digit",
            minute: "2-digit",
          });

          const formattedDateTime = `${formattedDate} ${formattedTime}`;
          console.log("formatted date:", formattedDateTime);

          frm.call({
            method: "show_branch_logs",
            freeze: true, // Set to true to freeze the UI
            freeze_message: "Please wait, processing data...",
            args: {
              self: frm.doc.name,
              date: formatcurrentDate,
            },
            callback: function (r) {
              if (!r.exc) {
                const data = r.message;
                console.log(data);

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
                          height: 60px;
                          text-align: center;
                          font-size: 15px;
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
                          border-bottom: 1px solid #D9D9D9;
                          height: 60px;
                      }

                      .branch-row_border:hover {
                          background-color: #c2d7df;
                          cursor: pointer;
                      }

                      .start-time {
                        color: green;
                        border: 2px solid green;
                        padding: 3px 10px;
                        border-radius: 2rem;
                        font-weight: 600;
                      }

                      .end-time {
                          color: red;
                          border: 2px solid red;
                          padding: 3px 10px;
                          border-radius: 2rem;
                          font-weight: 600;
                      }

                      .branch_heading {
                          display: flex;
                          justify-content: space-between;
                          align-items: start;

                      }

                      .startbtn{
                        background-color: green;
                        padding: 3px 10px;
                        border-radius: 1rem;
                        font-weight: 600;
                        color: white;
                        border: none;
                      }

                      .startbtn:focus{
                        outline:none;
                      }
                      .endbtn{
                        background-color: red;
                        padding: 3px 10px;
                        border-radius: 1rem;
                        font-weight: 600;
                        color: white;
                        border: none;
                      }
                      .endbtn:focus{
                        outline:none;
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
                  <script>
                  function startButton(branchName) {
                    console.log("Button click");
                
                    const branch = branchName;
                    console.log("Branch Name:", branch);
                
                    // Get the current user
                    const currentUser = frappe.session.user;
                    console.log("Current User:", currentUser);
                
                    // Extract user ID from the email address
                    const userId = currentUser.split('@')[0];
                    console.log("User ID:", userId);
                
                    // Fetch logged-in employee details
                    frappe.call({
                      method: "frappe.client.get_value",
                      args: {
                        doctype: "Employee",
                        filters: { user_id: currentUser },
                        fieldname: ["employee_name"]
                      },
                      callback: function (employeeResponse) {
                        if (!employeeResponse.exc) {
                          const employeeName = employeeResponse.message.employee_name;
                          console.log("Employee name", employeeName);
                
                          // call Check conditions method to check previous days complete and fetch date
                          frappe.call({
                            method: "share_holder_management.share_holder_management.doctype.day_management.day_management.check_conditions",
                            callback: function (response) {
                              // Callback function to handle the server's response
                              if (!response.exc) {
                                const data = response.message;
                                console.log("Response", data);
                                console.log("data", data);
                
                                const originalDate = data[0].Date;
                                console.log("inside script original date:", originalDate);

                                const originalDateParts = originalDate.split('-');
                                // Reformat the date as dd/mm/yyyy
                                const formattedOriginalDate = originalDateParts[2] +'/'+  originalDateParts[1] +'/'+ originalDateParts[0];

                                const currentDateTime = new Date();
                                const currentHour = currentDateTime.getHours().toString().padStart(2, '0');
                                const currentMinute = currentDateTime.getMinutes().toString().padStart(2, '0');

                                const currentTime = currentHour + ':' + currentMinute;
                                console.log("current time format:",currentTime)

                                const formattedDateTime = originalDate +','+ currentTime;
                                console.log("formatted date and time:", formattedDateTime);

                                // Combine the original date and current time
                                const modifiedDate = formattedOriginalDate +','+ currentTime;

                                console.log("final formatted date time:", modifiedDate);

                                // calling start branch day server function
                                frappe.call({
                                  method: "share_holder_management.share_holder_management.doctype.day_management.day_management.start_branch_day",
                                  args: {
                                    branch: branch,
                                    userId: userId,
                                    employeeName: employeeName,
                                    datetime_str:modifiedDate,
                                  },
                                  callback: function (response) {
                                    // Callback function to handle the server's response
                                    if (!response.exc) {
                                      const data = response.message;
                                      console.log("Response", data);
                                      // Check if emp_name is present in the response
                                      console.log("Employee Name:", data.emp_name);
                
                                      frappe.show_alert({
                                        message: __(branch + ' Branch started Successfully'),
                                        indicator: 'green'
                                      }, 5);
                
                                      // Delay the page reload by 2 seconds (adjust as needed)
                                      setTimeout(function () {
                                        // Refresh the page after the alert is shown
                                        location.reload();
                                      }, 1000);
                
                                    } else {
                                      // Handle errors
                                      console.error("Error:", response.exc);
                                    }
                                  }
                                });
                              } else {
                                // Handle errors or conditions not met
                                console.error("Error or conditions not met:", response.exc);
                              }
                            }
                          });
                        } else {
                          // Handle errors fetching employee details
                          console.error("Error fetching employee details:", employeeResponse.exc);
                        }
                      }
                    });
                  }

                  function endButton(branchName) {
                    console.log("End Button click");
                
                    const branch = branchName;
                    console.log("Branch Name:", branch);
                
                    // Get the current user
                    const currentUser = frappe.session.user;
                    console.log("Current User:", currentUser);
                
                    // Extract user ID from the email address
                    const userId = currentUser.split('@')[0];
                    console.log("User ID:", userId);
                
                    // Fetch logged-in employee details
                    frappe.call({
                        method: "frappe.client.get_value",
                        args: {
                            doctype: "Employee",
                            filters: { user_id: currentUser },
                            fieldname: ["employee_name"]
                        },
                        callback: function (employeeResponse) {
                            if (!employeeResponse.exc) {
                                const employeeName = employeeResponse.message.employee_name;
                                console.log("Employee name", employeeName);
                
                                // call Check conditions method to check previous days complete and fetch date
                                frappe.call({
                                    method: "share_holder_management.share_holder_management.doctype.day_management.day_management.check_conditions",
                                    callback: function (response) {
                                        // Callback function to handle the server's response
                                        if (!response.exc) {
                                            const data = response.message;
                                            console.log("Response", data);
                                            console.log("data", data);
                
                                            const originalDate = data[0].Date;
                                            console.log("inside script original date:", originalDate);
                
                                            const originalDateParts = originalDate.split('-');
                                            // Reformat the date as dd/mm/yyyy
                                            const formattedOriginalDate = originalDateParts[2] + '/' + originalDateParts[1] + '/' + originalDateParts[0];
                
                                            const currentDateTime = new Date();
                                            const currentHour = currentDateTime.getHours().toString().padStart(2, '0');
                                            const currentMinute = currentDateTime.getMinutes().toString().padStart(2, '0');
                
                                            const currentTime = currentHour + ':' + currentMinute;
                                            console.log("current time format:", currentTime);
                
                                            const formattedDateTime = originalDate + ',' + currentTime;
                                            console.log("formatted date and time:", formattedDateTime);
                
                                            // Combine the original date and current time
                                            const modifiedDate = formattedOriginalDate + ',' + currentTime;
                                            console.log("final formatted date time:", modifiedDate);
                
                                            // calling end branch day server function
                                            frappe.call({
                                                method: "share_holder_management.share_holder_management.doctype.day_management.day_management.end_branch_day",
                                                args: {
                                                    branch: branch,
                                                    userId: userId,
                                                    employeeName: employeeName,
                                                    datetime_str: modifiedDate,  // Use the correct parameter name expected by the server-side function
                                                },
                                                callback: function (response) {
                                                    // Callback function to handle the server's response
                                                    if (!response.exc) {
                                                        const data = response.message;
                                                        console.log("Response", data);
                                                        // Check if emp_name is present in the response
                                                        console.log("Employee Name:", data.emp_name);
                
                                                        frappe.show_alert({
                                                            message: __(branch + ' Branch ended Successfully'),
                                                            indicator: 'green'
                                                        }, 5);
                
                                                        // Delay the page reload by 2 seconds (adjust as needed)
                                                        setTimeout(function () {
                                                            // Refresh the page after the alert is shown
                                                            location.reload();
                                                        }, 1000);
                
                                                    } else {
                                                        // Handle errors
                                                        console.error("Error:", response.exc);
                                                    }
                                                }
                                            });
                                        } else {
                                            // Handle errors or conditions not met
                                            console.error("Error or conditions not met:", response.exc);
                                        }
                                    }
                                });
                            } else {
                                // Handle errors fetching employee details
                                console.error("Error fetching employee details:", employeeResponse.exc);
                            }
                        }
                    });
                }
                
              </script>

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
                                          : `<button class="startbtn" onclick="startButton('${row.branch}')">Start</button>`
                                      }</td>
                                      <td class="branch-td">${
                                        row.Day_Start_by || ""
                                      }</td>
                                      <td class="branch-td">${
                                        row.start_time
                                          ? row.end_time
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
                                            : `<button class="endbtn" onclick="endButton('${row.branch}')">End</button>`
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
                const branchSearchInput =
                  document.getElementById("branchSearch");
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
              } else {
                frappe.msgprint("Error fetching details");
              }
            },
          });
        }
      },
    });
  },

  // Modified code for date validation

  onload: function (frm) {
    frm.trigger("header_links");
    console.log("Onload");
  },
});
