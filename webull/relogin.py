from webull import webull
import json

def relogin(wb):
    fh = open('webull_credentials.json', 'r')
    credential_data = json.load(fh)
    fh.close()

    wb._refresh_token = credential_data['refreshToken']
    wb._access_token = credential_data['accessToken']
    wb._token_expire = credential_data['tokenExpireTime']
    wb._uuid = credential_data['uuid']

    n_data = wb.refresh_login()
    credential_data['refreshToken'] = n_data['refreshToken']
    credential_data['accessToken'] = n_data['accessToken']
    credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

    file = open('webull_credentials.json', 'w')
    json.dump(credential_data, file)
    file.close()

    print(wb.get_account_id())