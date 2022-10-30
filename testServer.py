import json, requests
from requests.exceptions import RequestException, HTTPError, URLRequired

def main():

  # Configuration Values
  domain = '<domain>'
  audience = f'https://{domain}/api/v2/'
  client_id = '<client_id>'
  client_secret = '<client_secret>'
  grant_type = "client_credentials" # OAuth 2.0 flow to use

  # Get an Access Token from Auth0
  base_url = f"https://{domain}"
  payload =  { 
    'grant_type': grant_type,
    'client_id': client_id,
    'client_secret': client_secret,
    'audience': audience
  }
  response = requests.post(f'{base_url}/oauth/token', data=payload)
  oauth = response.json()
  access_token = oauth.get('access_token')

  # Add the token to the Authorization header of the request
  headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
  menu(access_token,base_url)

def menu(access_token,base_url):
    value = input("Select option (1-3): \n 1. Query all Applications\n 2. Query Actions bound by Apps\n 3. Query Actions bound by Trigger")

    match value:
        case "1":
            queryApps(access_token,base_url) 
        case "2":
            getActions(access_token,base_url) 
        case "3":
            getActions_byTrigger(access_token,base_url)


def queryApps(access_token,base_url):
    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
    # Get all Applications using the token
    try:
        res = requests.get(f'{base_url}/api/v2/clients', headers=headers)
        print('\n')
        print("All Applications:")
        res = res.json()
        appList = ""
        for app in res:
            appList += app['name'] + ", "
        appList = appList[:-2]
        
        print(appList)
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('\n')
        menu(access_token,base_url)

    except HTTPError as e:
        print(f'HTTPError: {str(e.code)} {str(e.reason)}')
    except URLRequired as e:
        print(f'URLRequired: {str(e.reason)}')
    except RequestException as e:
        print(f'RequestException: {e}')
    except Exception as e:
        print(f'Generic Exception: {e}')
    print('--------------')
    menu(access_token,base_url)

def getActions(access_token,base_url):
    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
    try:
        res = requests.get(f'{base_url}/api/v2/actions/actions', headers=headers)
        res = res.json()
        actions_app_dic = {}
        for action in res['actions']:
            code = action['code']
            appname = filterString(code,access_token,base_url)
            actions_app_dic[action['name']] = appname
        print('\n')
        print('Returning all Actions by Apps...')
        print(actions_app_dic)
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('\n')
        menu(access_token,base_url)
    except HTTPError as e:
        print(f'HTTPError: {str(e.code)} {str(e.reason)}')
    except URLRequired as e:
        print(f'URLRequired: {str(e.reason)}')
    except RequestException as e:
        print(f'RequestException: {e}')
    
def filterString(code,access_token,base_url):
    is_client = code.find("event.client")
    is_client_name = code.find("event.client.name")

    #Action has App bounded
    if is_client != -1:
        codeString = code[is_client:]
        rightIndex = codeString.find('\n')
        subStr = codeString[:rightIndex]

        appNamesLastIndex = subStr.rfind('"')
        appNames = subStr[:appNamesLastIndex+1]

        #Remove all special characters
        appNames = appNames.replace('=','')
        appNames = appNames.replace('|','')

        #Convert to List
        appNamesList = appNames.split('  ')
        resList = []

        for i in range(len(appNamesList)):
            if appNamesList[i].strip(' "\'\t\r\n') == 'event.client.name':
                resList.append(appNamesList[i+1].strip(' "\'\t\r\n'))

            if appNamesList[i].strip(' "\'\t\r\n') == 'event.client.id':
                resList.append(convertIdToAppName(appNamesList[i+1].strip(' "\'\t\r\n'),access_token,base_url))
                
            else:
                pass
        return resList
    return ["Action is not bounded to any Client"]

def convertIdToAppName(string,access_token,base_url):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        }
    try:
        res = requests.get(f'{base_url}/api/v2/clients/{string}?fields=name&include_fields=true', headers=headers)
        res = res.json()

        # for client in res['name']:
        return res['name']
        
        
    except HTTPError as e:
        print(f'HTTPError: {str(e.code)} {str(e.reason)}')
    except URLRequired as e:
        print(f'URLRequired: {str(e.reason)}')
    except RequestException as e:
        print(f'RequestException: {e}')

    return ("Unable to find AppName")
# def getTriggerBindings(access_token,base_url):

def getActions_byTrigger(access_token,base_url):
    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
    try:
        res = requests.get(f'{base_url}/api/v2/actions/actions', headers=headers)
        res = res.json()
        actions_app_dic = {}
        for action in res['actions']:
    
            actionName = action['name']
            for anAttribute in action['supported_triggers']:
                trigger = anAttribute['id']
            actions_app_dic[actionName] = trigger
        print('\n')
        print('Returning all Actions by Trigger Bindings...')
        print(actions_app_dic)
    except HTTPError as e:
        print(f'HTTPError: {str(e.code)} {str(e.reason)}')
    except URLRequired as e:
        print(f'URLRequired: {str(e.reason)}')
    except RequestException as e:
        print(f'RequestException: {e}')
    except Exception as e:
        print(f'Generic Exception: {e}')
    print('------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('\n')
    menu(access_token,base_url)


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()