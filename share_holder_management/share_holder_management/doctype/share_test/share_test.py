import frappe
import socket
import fcntl
import struct
from frappe.model.document import Document

class ShareTest(Document):
    def before_save(self):
        self.set_mac_and_ip()

    def set_mac_and_ip(self):
        # Get the correct IP address from an active network interface
        ip_address = self.get_active_ip()

        # Get MAC address for the interface with the found IP address
        mac_address = self.get_mac_address(ip_address)

        # Assuming 'mac' and 'ip' fields exist in your doctype
        self.mac = mac_address
        self.ip = ip_address

    def get_active_ip(self):
        # Iterate over all interfaces and get the IP of the first active one (non-loopback)
        interfaces = socket.if_nameindex()
        for if_name, _ in interfaces:
            ip_address = self.get_ip_for_interface(if_name)
            if ip_address and not ip_address.startswith("127."):
                return ip_address
        return None

    def get_ip_for_interface(self, interface_name):
        try:
            ip_address = socket.inet_ntoa(fcntl.ioctl(
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', bytes(interface_name[:15], 'utf-8'))
            )[20:24])
            return ip_address
        except Exception as e:
            return None

    def get_mac_address(self, ip_address):
        # Retrieve the MAC address based on the IP address
        interface_name = self.get_interface_name(ip_address)
        if interface_name:
            mac_address = self.get_interface_mac(interface_name)
            return mac_address
        else:
            return "00:00:00:00:00:00"  # Return a default value if something goes wrong

    def get_interface_name(self, ip_address):
        interfaces = socket.if_nameindex()
        for if_name, _ in interfaces:
            try:
                # Check if this interface has the IP we're looking for
                if_ip = socket.inet_ntoa(fcntl.ioctl(
                    socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', bytes(if_name[:15], 'utf-8'))
                )[20:24])
                if if_ip == ip_address:
                    return if_name
            except Exception as e:
                continue
        return None

    def get_interface_mac(self, interface_name):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            mac_address = ':'.join(['{:02x}'.format(b) for b in fcntl.ioctl(
                s.fileno(),
                0x8927,  # SIOCGIFHWADDR
                struct.pack('256s', bytes(interface_name[:15], 'utf-8'))
            )[18:24]])
            return mac_address.upper()
        except Exception as e:
            return "00:00:00:00:00:00"  # Return a default value if something goes wrong



@frappe.whitelist()
def receive_xml_data():
    try:
        # Make a GET request to the API endpoint
        response = requests.get('https://mocktarget.apigee.net/xml')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)
            
            # Extract data from XML
            first_name = root.find('firstName').text
            last_name = root.find('lastName').text
            
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

    

import requests

import requests
import requests
import frappe

import requests
import frappe

import requests
import frappe

@frappe.whitelist()
def send_data():
    try:
        # Hardcoded values for testing
        first_name = "John"
        last_name = "Doe"
        
        # Construct XML data
        xml_data = f"<root><first_name>{first_name}</first_name><last_name>{last_name}</last_name></root>"
        
        # Print XML data being sent
        frappe.msgprint("XML Data Sent:\n" + xml_data)

        # Define the URL of the API endpoint
        url = 'http://192.168.1.252/api/method/simple.simple.api.submit_data'

        # Make the POST request to the API endpoint with XML data
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(url, data={'xml_data': xml_data}, headers=headers)

        # Print XML response received
        frappe.msgprint("XML Response Received:\n" + response.text)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return True, "Data submitted successfully"
        else:
            return False, "Data submission failed"
    except Exception as e:
        # Handle any exceptions that occur during the request
        frappe.log_error("Error sending data to API: {}".format(e))
        return False, f"Error: {e}"



import frappe
import requests
import xml.etree.ElementTree as ET

def create_customer():
    # Define the XML payload
    xml_payload = """
    <?xml version="1.0" encoding="UTF-8"?>
    <FIXML xsi:schemaLocation="http://www.finacle.com/fixml RetCustAdd.xsd" xmlns="http://www.finacle.com/fixml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <Header>
        <RequestHeader>
          <MessageKey>
            <RequestUUID>Req_163844373_3119</RequestUUID>
            <ServiceRequestId>RetCustAdd</ServiceRequestId>
            <ServiceRequestVersion>10.2</ServiceRequestVersion>
            <ChannelId>CRM</ChannelId>
            <LanguageId></LanguageId>
          </MessageKey>
          <RequestMessageInfo>
            <BankId>01</BankId>
            <TimeZone></TimeZone>
            <EntityId></EntityId>
            <EntityType></EntityType>
            <ArmCorrelationId></ArmCorrelationId>
            <MessageDateTime>2021-11-02T03:11:37.780</MessageDateTime>
          </RequestMessageInfo>
          <Security>
            <Token>
              <PasswordToken>
                <UserId></UserId>
                <Password></Password>
              </PasswordToken>
            </Token>
            <FICertToken></FICertToken>
            <RealUserLoginSessionId></RealUserLoginSessionId>
            <RealUser></RealUser>
            <RealUserPwd></RealUserPwd>
            <SSOTransferToken></SSOTransferToken>
          </Security>
        </RequestHeader>
      </Header>
      <Body>
        <RetCustAddRequest>
          <RetCustAddRq>
            <CustDtls>
              <CustData>
                <!-- Customer details -->
              </CustData>
            </CustDtls>
            <RelatedDtls>
              <!-- Related details -->
            </RelatedDtls>
          </RetCustAddRq>
        </RetCustAddRequest>
      </Body>
    </FIXML>
    """

    # Define the API endpoint
    api_url = "https://your-api-endpoint.com/RetCustAdd"

    # Send the POST request
    response = requests.post(api_url, data=xml_payload, headers={'Content-Type': 'application/xml'})

    # Check the response
    if response.status_code == 200:
        # Parse the response XML
        root = ET.fromstring(response.content)

        # Extract the relevant information from the response
        cust_id = root.find("./Body/RetCustAddResponse/RetCustAddRs/CustId").text
        desc = root.find("./Body/RetCustAddResponse/RetCustAddRs/Desc").text
        entity = root.find("./Body/RetCustAddResponse/RetCustAddRs/Entity").text
        service = root.find("./Body/RetCustAddResponse/RetCustAddRs/Service").text
        status = root.find("./Body/RetCustAddResponse/RetCustAddRs/Status").text

        # Create a new customer in Frappe
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Test Customer",
            "customer_group": "Individual",
            "territory": "All Territories",
            "customer_type": "Individual",
            "customer_id": cust_id
        })
        customer.insert()

        frappe.db.commit()

        print(f"Customer created successfully with CIFID: {cust_id}")
        print(f"Description: {desc}")
        print(f"Entity: {entity}")
        print(f"Service: {service}")
        print(f"Status: {status}")
    else:
        print(f"Error: {response.status_code} - {response.text}")