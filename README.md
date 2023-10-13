# BizEvent Pusher

A tool to assist pushing Business Events (aka bizevents) to the Dynatrace platform.

## New To Business Events?

[Watch Andi and Klaus's business event session on YouTube](https://www.youtube.com/watch?v=KuG3PniOaQs)

## Prereq: Create OAuth Client

Follow [the documentation here](https://www.dynatrace.com/support/help/platform-modules/business-analytics/ba-api-ingest) to set up an OAuth client + policy + bind to your service user account email.

## Use It

- Tenant must be WITHOUT trailing slash.
- `-ocid` = Client ID generated above
- `-ocs` = Client secret generated above
- `-urn` = URN generated above

```
docker run --rm ghcr.io/dynatrace-oss/bizevent-pusher:v1.1.1 \
-ten https://abc12345.live.dynatrace.com \
-ocid dt0s02.***** \
-ocs dt0s02.*****.**************** \
-urn urn:dtaccount:******** \
-p "{\"foo\": \"bar\"}"
```

Successful output should result in:

```
Bizevent successfully sent!
```

### Sample GitHub Action Workflow
This container can be used as part of a GitHub Action workflow. For example, to push a bizevent anytime an issue is `opened`, `edited` or `closed`.

Of course, first you need to create GitHub Action secrets to hold your details.

- `secrets.DT_TENANT_URL` like `https://abc12345.live.dynatrace.com` (no trailing slash)
- `secrets.DT_OAUTH_CLIENT_ID` like `dt0s02.*****`
- `secrets.DT_OAUTH_CLIENT_SECRET` like `dt0s02.****.*******`
- `secrets.DT_ACCOUNT_URN` like `urn:dtaccount:********`

```
name: send-biz-events
run-name: send-biz-events
on:
  issues:
    types: [opened, edited, closed]
  pull_request:
    types: [opened, edited, closed]
jobs:
  bizevent-push:
    runs-on: "ubuntu-latest"
    steps:
      - name: "Push Bizevent"
        env:
          TRIGGER: ${{ (github.event_name == 'issues') && 'issue' || 'pull_request' }}
        run: |
          URL=$(jq -r '${{ format('.event.{0}.html_url', env.TRIGGER) }}' <<< '${{ toJSON(github) }}')
          docker run --rm ghcr.io/dynatrace-oss/bizevent-pusher:v1.1.1 \
          -ten ${{ secrets.DT_TENANT_URL }} \
          -ocid ${{ secrets.DT_OAUTH_CLIENT_ID }} \
          -ocs ${{ secrets.DT_OAUTH_CLIENT_SECRET }} \
          -urn ${{ secrets.DT_ACCOUNT_URN }} \
          -p "{\"type\": \"${{ github.event_name }}.${{ github.event.action }}\", \"source\": \"githubactions\", \"data\": { \"id\": \"${{ github.event.issue.number }}\", \"title\": \"${{ github.event.issue.title }}\", \"link\": \"$URL\" } }"
```

## Retrieving Business Events
In the platform, run:

```
fetch bizevents
| filter isNotNull(type)
| filter type == "[issues|pull_request].[opened|edited|closed]"
```

## Clone and Build

Optional, but if you want to clone this repo and build a custom version:

```
git clone https://github.com/dynatrace-oss/bizevent-pusher.git
cd bizevent-pusher
docker build -t YOU/bizevent-pusher:dev code/.
```
