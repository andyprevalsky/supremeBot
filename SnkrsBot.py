import sys,json,requests
from bs4 import BeautifulSoup as bs
import webbrowser
from requests.utils import dict_from_cookiejar

def setup_session(username, password, sess):
    sess.get("https://store.nike.com/us/en_us/?l=shop,login")

    payload = { 
        "client_id" : "PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7",
        "grant_type" : "password",
        "keepMeLoggedIn" : "true",
        "password" : password,
        "username" : username,
        "ux_id" : "com.nike.commerce.snkrs.web"
    }
    response = sess.post('https://unite.nikecloud.com/login?locale=en_US&backendEnvironment=identity', data = json.dumps(payload))
 
    sess.get("https://www.nike.com/launch/")

    return 

if __name__ == "__main__":

    accounts = {
        "iprevalsky@gmail.com" : "Cowboys1",
        "andyprevalsky@yahoo.com" : "Rockey181818",
        "georgeprevalsky@gmail.com" : "Rockey181818"
    }
    z = 0
    for key in accounts:
        z+= 1
    session_list = ['*']*z
    i = 0
    for key, value in accounts.items():
        session_list[i] = requests.session()
        setup_session(key, value, session_list[i])

def accout_billing(username)
    billing_dict1 = {
        
    }
    if username = "iprevalsky@gmail.com"
        return billing_dict1
    if username = "andyprevalsky@yahoo.com"
        return billing_dict2
    if username = "georgeprevalsky@gmail.com"
        return billing_dict3