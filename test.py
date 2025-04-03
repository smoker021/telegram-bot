   import requests
   url = "https://api.telegram.org/bot7924841546:AAEQEO5K2xy-77wwAtnKe1GhhYrO75LXvmU/getMe"
   response = requests.get(url)
   print(response.text)
   
