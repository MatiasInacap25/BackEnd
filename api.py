import requests

# Where USD is the base currency you want to use
url = 'https://v6.exchangerate-api.com/v6/9f92a658f32a5c886cbf89af/pair/CLP/EUR/1000'

# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)