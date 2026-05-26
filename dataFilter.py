# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from dataMerger import merger
import pandas as pd

def adsb_filter():
    data, numAc = merger()
        
    AcType = []
    AcReg = []
    callsign = []
    lon = []
    lat = []
    alt = []
    speed = []
    emergency = []
    military = []
    year = []
    owner = []
    
    for i in data.itertuples():
        AcType.append(i.t)
        AcReg.append(i.r)
        callsign.append(i.flight.strip() if isinstance(i.flight, str) else 'N/A')        
        lon.append(i.lon)
        lat.append(i.lat)
        alt.append(i.alt_baro)
        speed.append(i.gs)   
        emergency.append(i.emergency if isinstance(i.emergency, str) else 'none')
        military.append(True if (pd.notna(i.dbFlags) and isinstance(i.dbFlags, (int, float)) and int(i.dbFlags) & 1) else False)
        year_val = getattr(i, 'year', None)
        owner_val = getattr(i, 'ownOp', None)
        
        if pd.notna(year_val) and year_val != '':
            try:
                year.append(str(int(float(year_val))))
            
            except (ValueError, TypeError):
                year.append('N/A')
        
        else: 
            year.append('N/A')
        
        if pd.notna(owner_val):
            cleaned_owner = str(owner_val).strip()
            
            if cleaned_owner != '' and cleaned_owner.lower() not in ('nan', 'none'):
                owner.append(cleaned_owner)
            
            else:
                owner.append('N/A')
        
        else:
            owner.append('N/A')

    return numAc, AcType, AcReg, callsign, alt, speed, lat, lon, emergency, military, year, owner
    
