import requests
import json
import aciCredentials
import urllib3

urllib3.disable_warnings()


# declare variables
url = str(aciCredentials.url) + "/api/aaaLogin.json"
user = str(aciCredentials.user)
pword = str(aciCredentials.pwd)


#url = "https://10.231.201.21/api/aaaLogin.json"

# payload = "{\r\n    \"aaaUser\" : {\r\n        \"attributes\" : {\r\n            " \
#           "\"name\" : \"apic:DataComm\\\\bhoward99\",\r\n            \"pwd\" : \"Sh0tei01\"\r\n        }" \
#           "\r\n    }\r\n}"


payload = "{\r\n    \"aaaUser\" : {\r\n        \"attributes\" : {\r\n            " \
          "\"name\" : \"apic:DataComm\\\\bhoward99\",\r\n            \"pwd\" : \"Sh0tei01\"\r\n        }" \
          "\r\n    }\r\n}"

headers = {'Content-Type': 'application/json'}


# response is JSON format returned from the request
response = requests.request("POST", url, verify=False, headers=headers, data=payload)

# response.text converts JSON format to a string
# json.loads converts the JSON string to a python dictionary
json_response = json.loads(response.text)

# extracts the token from the Python dictionary
token = json_response['imdata'][0]['aaaLogin']['attributes']['token']





