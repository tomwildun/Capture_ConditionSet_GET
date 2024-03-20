import requests

# Define contract mappings
contract_mappings = [
    {'necBillingCode': 'NECXXX-XX', 'conditionSetName': 'Hospital Condition Set 3'}
]

# Define authentication token and API URLs
auth_token = ''
URL = 'https://beta.capturerx.com/apiservice/cumulus/v1/contracts/'
condition_set_URL = 'https://beta.capturerx.com/apiservice/cumulus/v1/condition_sets/'

# Define header with authorization token
header = {'Authorization': 'Bearer ' + auth_token}

# Get condition sets and contracts from API
response = requests.get(condition_set_URL, headers=header)
condition_sets = response.json()

response2 = requests.get(URL, headers=header)
contracts = response2.json()

failures = []

# Iterate through contract mappings
for mapping in contract_mappings:
    condition_set_to_add = {}
    # Find matching condition set
    for condition_set in condition_sets:
        if condition_set['name'] == mapping['conditionSetName']:
            condition_set_to_add = condition_set
            break
        
    contract_to_update = {}
    # Find matching contract
    for contract in contracts:
        if contract['necBillingCode'] == mapping['necBillingCode']:
            contract_to_update = contract
            break
    
    # If contract found, update its condition set
    if(bool(contract_to_update) != False):
        response3 = requests.get(URL + contract_to_update['id'], headers=header)
        contract = response3.json()    
        contract['conditionSetId'] = condition_set_to_add['id']
        body = contract
    
        final_response = requests.put(URL, json=body, headers=header)
        print(final_response)
        print(final_response.text)
    else:
        failures.append(mapping['necBillingCode'] + '\t' + mapping['conditionSetName'])
        print(failures)
