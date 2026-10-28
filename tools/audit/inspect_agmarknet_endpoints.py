import requests, re

r = requests.get('https://agmarknet.gov.in/static/js/main.c1f86740.js', timeout=10)
# Find endpoints under api.agmarknet.gov.in
matches = re.findall(r'api\.agmarknet\.gov\.in/v1/([a-zA-Z0-9_\-\/\?&=]+)', r.text)
print('Direct matches:', set(matches))

# Also search for api calls like .get( or .post( or endpoint constants
endpoints = re.findall(r'["\'](/?[a-zA-Z0-9_\-]+(?:commodity|market|price|state|district|daily)[a-zA-Z0-9_\-\/]*)["\']', r.text)
print('Other endpoints:', set(endpoints))
