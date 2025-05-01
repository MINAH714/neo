import requests
from urllib.parse import urlencode

CLIENT_ID = 'GeujpxISRCAGwtvRRwu67Scqot5VVSGx'
CLIENT_SECRET = 'mNVQG01ruRq7GptO'

def get_amadeus_access_token(client_id, client_secret):
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, headers=headers, data=urlencode(data))
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"Access Token: {access_token}")
        return access_token
    else:
        print("토큰 요청 실패:", response.status_code)
        print(response.text)
        return None

if __name__ == "__main__":
    token = get_amadeus_access_token(CLIENT_ID, CLIENT_SECRET)