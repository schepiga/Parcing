# Задание 1
import requests
import json

url = 'https://api.github.com'
user = 'octokit'
req = requests.get(f'{url}/users/{user}/repos')
data = json.loads(req.text)
print(f" Перечень репозитеориев пользователя {user}:")
for i in req.json():
    print(i['name'])

# Задание 2
url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=Q5mHPo2yDG8&key={YOUR_API_KEY}'
YOUR_API_KEY = 'AIzaSyBb8wfalvcaRS3I175DEUi7c6sPMMipmuE'
response = requests.get(url)
j_data = response.json()
print(j_data)