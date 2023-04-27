# BizEvent Pusher

A tool to assist pushing Business Events (aka bizevents) to the Dynatrace platform.

## Prereq: Create OAuth Client

1. Go to the [Dynatrace account management API page](https://account.dynatrace.com/my/enterprise-api)
2. Click "Create New Client"
3. Provide a descriptive name and use your email as the service user ID
4. Uncheck all **Account** permissions
5. Switch to **Grail data ingest** tab and check **Write/edit events (storage:events:write)**
6. Double check that the **only** box you have checked in the **storage:events:write** box
7. Click **Generate new client**
8. Make a note of the 3 values provided (client ID, client secret and URN). These are sensitive. Do not store in Git.

## Use It

- Tenant must be WITHOUT trailing slash.
- `-ocid` = Client ID generated above
- `-ocs` = Client secret generated above
- `-urn` = URN generated above

```
docker run \
-ten https://abc12345.live.dynatrace.com \
-ocid dt0s02.***** \
-ocs dt0s02.*****.**************** \
-urn urn:dtaccount:******** \
-p '{"foo": "bar"}'
```

Successful output should result in:

```
Bizevent successfully sent!
```

## Retrieving Business Events
In the platform, run `fetch bizevents`.