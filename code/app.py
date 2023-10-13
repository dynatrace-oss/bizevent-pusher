import sys
import requests
import argparse
import json

#############################################################################
# USAGE TODO
# python app.py \
# -ten=https://abc12345.live.dynatrace.com \
# -ocid=dt0s02.**** \
# -ocs=dt0s02.***.*** \
# -urn=urn:dtaccount:UUID \
# -p="{VALID CLOUD EVENT ESCAPED JSON}"
#############################################################################

parser = argparse.ArgumentParser()

# Notes:
# You can use either short or long (mix and match is OK)
# Hyphens are replaced with underscores hence for retrieval
# and leading hyphens are trimmed
# --oauth-client-id becomes args.oauth_client_id
# Retrieval also uses the second parameter
# Hence args.account_urn will work but args.urn won't

# Sample values
# tenant_url = "https://abc12345.live.dynatrace.com" # No trailing slash
# oauth_client_id = "dt0s02.*****"
# This is sensitive! Store securely. DO NOT COMMIT TO GIT!
# oauth_client_secret = "dt0s02.*****.*****"
# This is sensitive! Store securely. DO NOT COMMIT TO GIT!
# account_urn = "urn:dtaccount:*******"
# permissions = "storage:bizevents:read storage:buckets:read storage:events:write"

# The following won't (often) change (if at all)
OAUTH_DEV_ENDPOINT = "https://sso-dev.dynatracelabs.com/sso/oauth2/token"
OAUTH_SPRINT_ENDPOINT = "https://sso-sprint.dynatracelabs.com/sso/oauth2/token"
OAUTH_PROD_ENDPOINT = "https://sso.dynatrace.com/sso/oauth2/token"
# default to "prod"
oauth_endpoint =  OAUTH_PROD_ENDPOINT
permissions = "storage:bizevents:read storage:buckets:read storage:events:write"

# Add arguments to script that user must pass
parser.add_argument('-ten', '--tenant', required=True)
parser.add_argument('-ocid', '--oauth-client-id', required=True)
parser.add_argument('-ocs', '--oauth-client-secret', required=True)
parser.add_argument('-p', '--payload', required=True)
parser.add_argument('-urn', '--account_urn', required=True)
parser.add_argument('-x', '--debug', required=False, default="False")

# Parse the arguments
args = parser.parse_args()
tenant_url = args.tenant
oauth_client_id = args.oauth_client_id
oauth_client_secret = args.oauth_client_secret
account_urn = args.account_urn
payload = json.loads(args.payload)
debug_mode = args.debug

# Use incoming tenant_url to set the biz event ingest URL
biz_event_url = f"{tenant_url}/api/v2/bizevents/ingest"

# Change OAuth endpoint based on environment
# Currently supports "dev", "sprint" or "prod" (default)
if ".dev." in tenant_url.lower():
    oauth_endpoint = OAUTH_DEV_ENDPOINT
if ".sprint." in tenant_url.lower():
    oauth_endpoint = OAUTH_SPRINT_ENDPOINT

# Set up debug mode and dry run switches
DEBUG_MODE = False
if debug_mode.lower() == "true":
   print("> Debug mode is ON")
   DEBUG_MODE = True

# Set up the OAuth body payload
oauth_body = {
    "grant_type": "client_credentials",
    "client_id": oauth_client_id,
    "client_secret": oauth_client_secret,
    "resource": account_urn,
    "scope": permissions
}

# Print debugging info if in debug mode
if DEBUG_MODE:
    print(f"Tenant URL: {tenant_url}")
    print(f"OAuth Endpoint: {oauth_endpoint}")
    print(f"OAuth Client ID: {oauth_client_id}")
    print(f"OAuth Body: {oauth_body}")
    print(f"Payload: {payload}")
    print(f"Debug: {debug_mode}")

##############################
# Step 1: Get Access Token
##############################
access_token_resp = requests.post(
    url=oauth_endpoint,
    data=oauth_body
)

if access_token_resp.status_code != 200:
    print(f"{access_token_resp.json()}")
    print("OAuth error occurred. Bizevent NOT sent. Please investigate.")
    exit(1)

access_token_json = access_token_resp.json()
access_token_value = access_token_json['access_token']

################################################
# Step 2: Use Access Token to push bizevent
################################################
biz_event_url = f"{tenant_url}/api/v2/bizevents/ingest"
biz_event_headers = {
    "Authorization": f"Bearer {access_token_value}"
}

biz_event_resp = requests.post(
    headers=biz_event_headers,
    url=biz_event_url,
    json=payload
)

if biz_event_resp.status_code == 202:
    print("Bizevent successfully sent!")
else:
    print(f"{biz_event_resp.json()}")
    print(f"Error sending bizevent. Please investigate. Exiting.")
    exit(1)
