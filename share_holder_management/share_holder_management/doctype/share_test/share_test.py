import frappe
import requests

from frappe.model.document import Document

class ShareTest(Document):
    pass

@frappe.whitelist()
def receive_data():
    try:
        # Make a GET request to the API endpoint
        response = requests.get('https://dummyjson.com/users')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Process the received data
            users = data.get('users', [])
            for user in users:
                # Extract first_name and last_name from the user data
                first_name = user.get('firstName')
                last_name = user.get('lastName')
                
                # Create a new ShareTest document with first_name and last_name
                share_test = frappe.new_doc('Share Test')
                share_test.first_name = first_name
                share_test.last_name = last_name
                
                # Insert the document into the database
                share_test.insert()
            
            return True
        else:
            frappe.log_error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return False
    except Exception as e:
        # Handle any exceptions that occur during the request
        frappe.log_error(f"Error receiving data from API: {e}")
        return False

    

@frappe.whitelist()
def send_data(first_name, last_name):
    # Define the data to be sent in the request body using the passed arguments
    data = {'first_name': first_name, 'last_name': last_name}

    # Define the URL of the API endpoint
    url = 'http://192.168.1.252/api/method/simple.simple.api.submit_data'

    try:
        # Make the POST request to the API endpoint
        response = requests.post(url, json=data)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        # Handle any exceptions that occur during the request
        frappe.log_error(f"Error sending data to API: {e}")
        return False

