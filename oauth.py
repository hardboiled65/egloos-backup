#!/usr/bin/python3
from requests_oauthlib import OAuth1Session

request_token_url = 'http://api.egloos.com/request_token'
base_authorization_url = 'http://api.egloos.com/authorize'
access_token_url = 'http://api.egloos.com/access_token'

def get_request_token(client_key, client_secret):
    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    return {
        'oauth_session': oauth,
        'oauth_token': resource_owner_key,
        'oauth_token_secret': resource_owner_secret,
    }

def get_oauth_verifier(oauth_session):
    authorization_url = oauth_session.authorization_url(base_authorization_url)
    print('visit the page and authorize: ')
    print(authorization_url)
    redirect_response = input('paste the full redirect URL: ')
    # oauth_response = oauth_session.parse_authorization_response(redirect_response)
    # verifier = oauth_response.get('verifier')
    verifier = redirect_response.split(sep='=')[2]

    return verifier

def get_access_token(client_key, client_secret, request_token, request_secret,
                        verifier):
    oauth = OAuth1Session(client_key, client_secret=client_secret,
        resource_owner_key=request_token, resource_owner_secret=request_secret,
        verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return {
        'oauth_token': resource_owner_key,
        'oauth_token_secret': resource_owner_secret,
    }

def request(client_key, client_secret, access_key, access_secret, url):
    oauth = OAuth1Session(client_key, client_secret=client_secret,
        resource_owner_key=access_key, resource_owner_secret=access_secret)
    r = oauth.get(url)

    return r
