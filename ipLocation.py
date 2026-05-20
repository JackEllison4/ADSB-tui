import requests

page = "https://ipapi.co/json/"

def location():
    getData = requests.get(page)
    data = getData.json()
    lat = data["latitude"]
    lon = data["longitude"]    
    return lon, lat
