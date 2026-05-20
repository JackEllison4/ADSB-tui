import requests

from ipLocation import location

lon, lat = location()

page = f"https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/250"

def colector():
    getData = requests.get(page)
    data = getData.json()
    return data