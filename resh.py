import requests


url = 'https://api.github.com/users/asdgds'
r = requests.get(url=url)
data = r.json()

print(type(data))
print(data)