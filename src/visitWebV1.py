import requests

url = "https://bing-web-search1.p.rapidapi.com/search"

querystring = {"mkt":"en-us","safeSearch":"Off","textFormat":"Raw","freshness":"Day"}

headers = {
	"x-rapidapi-key": "Sign Up for Key",
	"x-rapidapi-host": "bing-web-search1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())