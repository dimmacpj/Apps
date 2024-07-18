import requests
import time
url = "http://172.31.251.1"  
start_time = time.time()
response = requests.get(url)
print(response.text)
end_time = time.time()
loading_time = end_time - start_time
print(f"The loading time for the website {url} is {loading_time} seconds.")