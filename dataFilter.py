# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

def adsb_filter(data):
    numAc = data['total']
    dataAC = data['ac']
    
    AcType = []
    AcReg = []
    callsign = []
    lon = []
    lat = []
    alt = []
    speed = []
    emergency = []
    
    for i in dataAC:
        AcType.append(i.get('t'))
        AcReg.append(i.get('r'))
        callsign.append(i.get('flight'))
        lon.append(i.get('lon'))
        lat.append(i.get('lat'))
        alt.append(i.get('alt_baro'))
        speed.append(i.get('gs'))   
        emergency.append(i.get('emergency')) 

    return numAc, AcType, AcReg, callsign, alt, speed
    