# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import requests

from ipLocation import location

lon, lat = location()

page_lol = f"https://api.adsb.lol/v2/point/{lat}/{lon}/250"
page_fi = f"https://opendata.adsb.fi/api/v3/lat/{lat}/lon/{lon}/dist/250"
page_live = f"https://api.airplanes.live/v2/point/{lat}/{lon}/250"

def colector():
    headers = {"User-Agent": "ADSB-tui/1.0 (terminal client)"}
    
    try:
        getDataLOL = requests.get(page_lol, headers=headers, timeout=10)
        dataLOL = getDataLOL.json() if getDataLOL.status_code == 200 else {"total": 0, "ac": []}
    
    except Exception:
        dataLOL = {"total": 0, "ac": []}

    try:
        getDataFI = requests.get(page_fi, headers=headers, timeout=10)
        dataFI = getDataFI.json() if getDataFI.status_code == 200 else {"total": 0, "ac": []}
    
    except Exception:
        dataFI = {"total": 0, "ac": []}

    try:
        getDataLive = requests.get(page_live, headers=headers, timeout=10)
        dataLive = getDataLive.json() if getDataLive.status_code == 200 else {"total": 0, "ac": []}
    
    except Exception:
        dataLive = {"total": 0, "ac": []}

    return dataLOL, dataFI, dataLive

#-------------------------------------------------------------------
# Debugging
#-------------------------------------------------------------------

if __name__ == "__main__":
    print(colector())