# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import requests

page = "http://ip-api.com/json/"

def location():
    getData = requests.get(page)
    data = getData.json()
    lat = data["lat"]
    lon = data["lon"]    
    return lon, lat

#print(location()) #Debugging