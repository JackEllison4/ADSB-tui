# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import requests

from ipLocation import location

lon, lat = location()

page = f"https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/250"

def colector():
    getData = requests.get(page)
    data = getData.json()
    return data