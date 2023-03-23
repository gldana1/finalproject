import requests

url = "https://imdb8.p.rapidapi.com/auto-complete"

querystring = {"q":"office"}

headers = {
	"X-RapidAPI-Key": "de32aed7c6mshc427496794b63e2p151e0fjsn9afca0074b65",
	"X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)