import http.client
import json

conn = http.client.HTTPConnection("api.msg91.com")
authkey = "auth_key_here"

# Check Balance
def balance():
    conn.request("GET", "/api/balance.php?authkey="+authkey+"&type=4")
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Utility function to get group ID by group name
def idByName(name):
    groups = listGroups()

    for group in groups:
        if group['name'].lower() == name.lower():
            return group['id']
    
    return None

# sending message to a group
def sendToGroup(message, name):
    group_id = idByName(name)
    contacts = listContacts(group_id)
    numbers = []
    for contact in contacts:
        try:
            numbers.append(str(contact['number']))
        except:
            pass
    
    print(send(message, numbers))


# Sending a message
def send(message, numbers, flash='0'):
    payload = {}
    payload['sender'] = 'SASLPL'
    payload['route'] = '4'
    payload['country'] = '91'
    payload['flash'] = flash
    sms = {}
    sms['message'] = "SAFE & SECURE LOGISTICS PVT. LTD. \n HELLO "
    sms['to'] = numbers
    payload['sms'] = [sms] 

    payload = json.dumps(payload)
    headers = {
        'authkey': authkey,
        'content-type': "application/json"
        }

    conn.request("POST", "/api/v2/sendsms?country=91", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

# Adding a Group
def addGroup(group_name):
    URL = "/api/add_group.php?authkey="+authkey+"&group_name="+group_name
    conn.request("GET", URL)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Delete Group
def deleteGroup(group_id):
    conn.request("GET", "/api/delete_group.php?authkey="+authkey+"&group_id="+group_id)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Add Contact
def addContact(name, mob_no, group_id):
    URL = "/api/add_contact.php?authkey="+authkey+"&name="+name+"&mob_no="+str(mob_no)+"&group="+group_id
    conn.request("GET", URL)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
    
# Delete Contact
def deleteContact(contact_id):
    conn.request("GET", "/api/delete_contact.php?authkey="+authkey+"&contact_id="+contact_id)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
    
# List Groups
def listGroups():
    conn.request("GET", "/api/list_group.php?authkey="+authkey)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# List contacts
def listContacts(group_id):
    conn.request("GET", "/api/list_contact.php?group="+group_id+"&authkey="+authkey)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
