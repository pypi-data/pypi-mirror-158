# PyWaveApps
An API connector for the WaveApps platform (https://www.waveapps.com/) based on the WaveApps API (https://developer.waveapps.com/hc/en-us/categories/360001114072).
## Install
```pip3 install PyWaveApps```

Please note that use of this package may be subject to additional terms and conditions from WaveApps, including:
- https://www.waveapps.com/legal/terms-of-service-api-by-wave
- https://developer.waveapps.com/hc/en-us/articles/360020596571-Permitted-Use-Wave-Business-Owners
- https://developer.waveapps.com/hc/en-us/articles/360020596771-Permitted-Use-Developers-and-Integrators
## Quickstart
### Get Access Token
Currently, PyWaveApps only supports Full Access Token (bearer token) authentication. To obtain one, follow the steps below (based off of https://developer.waveapps.com/hc/en-us/articles/360018856751-Authentication):
1. Log into the developer portal: 
2. Create a new application or enter an existing one: https://developer.waveapps.com/hc/en-us/articles/360019762711
3. Scroll to the "Full Access tokens" section and click the "Create token" button to generate a new full access token.
### Setup
```
from pywaveapps import WaveApps

WAVE_APPS_BEARER_TOKEN = "<YOUR TOKEN HERE>"

wave = WaveApps(WAVE_APPS_BEARER_TOKEN)
...
```
### Query
There are several predefined functions to make integrating with WaveApps as quick as possible. Additionally, you can use the ```WaveApps.query.custom(..., **kwargs)``` method to pass your own query-string, and use ```kwargs``` to pass any variables.
```
...
wave.query.wave.query.businesses(...)
wave.query.customers(...)
wave.query.invoices(...)
wave.query.invoices_by_customer(...)
wave.query.user(...)

wave.query.custom(...)
...
```
###Mutate
Support for mutations is coming soon!

