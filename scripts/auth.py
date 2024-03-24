import streamlit as st
from msal_streamlit_authentication import msal_authentication

def azure_ad_auth(key, show_loggedin_page, allowed_users=[]):
    login_token = msal_authentication(
        auth={
            "clientId": "fa9c689d-f7cf-4607-98d8-53a6a0927986",
            "authority": "https://login.microsoftonline.com/1502e572-30a9-464c-b7f2-651dda344609",
            "redirectUri": "/",
            "postLogoutRedirectUri": "/"
        },
        cache={
            "cacheLocation": "sessionStorage",
            "storeAuthStateInCookie": False
        },
        login_request={
            "scopes": ["User.Read"]
        },
        logout_request={}, # Optional
        login_button_text="Login with Microsoft AD", # Optional, defaults to "Login"
        logout_button_text="Logout", # Optional, defaults to "Logout"
        class_name="css_button_class_selector", # Optional, defaults to None. Corresponds to HTML class.
        html_id="html_id_for_button", # Optional, defaults to None. Corresponds to HTML id.
        key=key # Optional if only a single instance is needed
    )
    uid = None
    if login_token:
        uid = login_token.get('account', {}).get('homeAccountId', None)
    print(uid)

    account_warning = st.empty()
    if show_loggedin_page:
        account_warning.warning(f':green[**Please use**] :blue[Micorsoft Account] to login.')

    email, username, full_name = None, None, None

    if login_token is not None:
        full_name = login_token['account']['name']
        email = login_token['account']['username']
        username, domain = email.split('@')

        # if str(domain).lower() != 'xl.co.id':
        #     st.error(f'Use xl.co.id account to login. Your domain {domain} is not accepted.')
        #     email, username, full_name = None, None, None

    success = None not in [username, full_name]

    if show_loggedin_page:
        if success:
            account_warning.empty()
            st.success(f'You have been authenticated as **"{full_name} ({email})"** using Microsoft AD')
            return email, username, full_name, uid
    
    elif success == False:
        st.warning(f'You are not authenticated using Microsoft AD.')

    else:
        if len(allowed_users) > 0 and (username not in allowed_users):
            account_warning.empty()
            st.error(f'**"{full_name}"** does not have access to this project!')
            st.info(f'Why are you viewing this page? Because this feature may be exclusive to only a few users.')
            return None, None, None, None
        
        return email, username, full_name, uid
    
    return email, username, full_name, uid
