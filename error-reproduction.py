import os

import requests
from dotenv import load_dotenv


load_dotenv()


def authorize():
    api_token = os.environ.get('RHEL_TOKEN')
    token_request = requests.post(
        'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token',
        data= {'grant_type': 'refresh_token', 'client_id': 'rhsm-api', 'refresh_token': api_token},
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    )
    if token_request.status_code == 200:
        token = token_request.json()['access_token'];
        print("Access Token Status:", token_request.status_code)
        return { 'Authorization': f'Bearer {token}' }
    raise Exception('Error connecting to Red Hat API. Please try again.')


def list_accounts():
    print("Account Lookups - this should return several users")
    account_number = os.environ.get('RHEL_ACCOUNT')
    headers = authorize()
    response = requests.get(
        f'https://api.access.redhat.com/account/v1/accounts/{account_number}/users',
        headers=headers
    )
    print("Account List Status:", response.status_code)
    print("Account List Results:", response.text)
    print()


def create_account():
    print("Account Activation - this should succeed")
    account_number = os.environ.get('RHEL_ACCOUNT')
    headers = authorize()

    data = {
        'username': 'test-user@tamu.edu',
        'firstName': 'Joe',
        'lastName': 'Aggie',
        'address': {
            'city': 'College Station',
            'country': 'US',
            'state': 'TX',
            'county': 'Brazos',
            'streets': ['3142 TAMU'],
            'zipCode': '77843'
        },
        'email': 'test-user@tamu.edu',
        'phone': '9798458300',
        'roles': [],
        'permissions': ['portal_download', 'portal_manage_cases']
    }
    validation_result = requests.post(
            f'https://api.access.redhat.com/account/v1/accounts/{account_number}/users?validateUser=true',
            json=data,
            headers=headers
    )
    if validation_result.status_code != 204:
        print("Validation Failed!")
        print(validation_result.status_code)
        print(validation_result.json())

    # We don't actually get to this point before running into the error, but this code would finish activating the account.
    #        
    #else:
    #    activation_result = requests.post(
    #        f'https://api.access.redhat.com/account/v1/accounts/{account_number}/users',
    #        json=data,
    #        headers=headers
    #    )
    #    if (activation_result.status_code == 200):
    #        print("Success!")
    #    else:
    #        print(activation_result.status_code)
    #        print(activation_result.text)


if __name__ == '__main__':
    list_accounts()
    create_account()
