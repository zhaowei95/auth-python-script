# Python Script to call Management API

This Script follows the Python Implementation to Get Management API Access Tokens for Production. 
https://auth0.com/docs/secure/tokens/access-tokens/get-management-api-access-tokens-for-production

### Installation
You can install the dependencies used in this script using the following command.
```
pip install -r requirements.txt
```

### API Access Token for Production
To retrieve the token, you first need to register a Machine-To-Machine application and replace these values based on your application.
https://auth0.com/docs/get-started/auth0-overview/create-applications/machine-to-machine-apps
```python
  domain = '<domain>'
  audience = f'https://{domain}/api/v2/'
  client_id = '<client_id>'
  client_secret = '<client_secret>'
  grant_type = "client_credentials" # OAuth 2.0 flow to use
```

### Methods in this script
This Python script contains 3 functions which uses the Management API Token and calls the Management Endpoint API. To retrieve the query, enter 1-3 in user-input for specific function to run.


#### 1. Query all Applications
Calls a GET on url/api/v2/clients
Returns a list of Applications in your Tenant.



#### 2. Query Actions bound by Apps
Calls a GET on url/api/v2/actions/actions
Returns a Dictionary of Actions key and list of Apps value.

'ActionName': ['App1','App2']

Actions that are not bounded to any application will have the value 'Action is not bounded to any Client'

The Function filters based on this naming convention as listed here:
For example: The "Allow access only on weedays for a specific application" sample Action here: 
https://auth0.com/docs/manage-users/access-control/sample-use-cases-actions-with-authorization


#### 3. Query Actions bound by Trigger
Calls a GET on url/api/v2/actions/actions
Returns a Dictionary of Actions key and String value of Trigger Binding.
'ActionName': 'post-login'


### Sample Outputs
When script is started, user will be prompted to input a value (1-3).<img width="677" alt="menu" src="https://user-images.githubusercontent.com/39029549/198880599-012615e9-eff7-4717-a64e-e790a6783584.png">

When '1' is chosen:
<img width="1058" alt="output1" src="https://user-images.githubusercontent.com/39029549/198880710-3add8d2d-02ce-4027-8be2-9e334e0bf3f7.png">

When '2' is chosen:
<img width="1063" alt="output2" src="https://user-images.githubusercontent.com/39029549/198880754-6de005de-24bc-4151-941d-5aabcdd9a2a5.png">

When '3' is chosen:
<img width="1067" alt="output3" src="https://user-images.githubusercontent.com/39029549/198880746-c483d3bc-9c05-4ba8-b9b8-8912941b737e.png">

### Sample Test Cases for retrieving Actions bound by App
Multiple reference to event.client.name
```
exports.onExecutePostLogin = async (event, api) => {
  if (event.client.name === "Default App" || event.client.name === "JS-App" || event.client.name === "App3") {
    const d = new Date().getDay();

    if (d === 0 || d === 6) {
      api.access.deny("This app is only available during the week.");
    }
  }
}
```
Multiple reference to event.client.name and event.client.id
```
exports.onExecutePostLogin = async (event, api) => {
  if (event.client.name === "API Explorer Application" || event.client.id === "ADdX3maj6JowxLyIfWqLBq5q8jkot7cC") {
    const d = new Date().getDay();

    if (d === 0 || d === 6) {
      api.access.deny("This app is only available during the week.");
    }
  }
}
```
