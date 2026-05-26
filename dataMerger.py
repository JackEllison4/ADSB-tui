# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import pandas as pd
from dataCollector import colector

def merger():
    dataLOL, dataFI, dataLive = colector()
    
    numAcLOL = dataLOL.get('total', 0) if isinstance(dataLOL, dict) else 0
    dataACLOL = dataLOL.get('ac', []) if isinstance(dataLOL, dict) else []
    numAcLive = dataLive.get('total', 0) if isinstance(dataLive, dict) else 0
    dataACLive = dataLive.get('ac', []) if isinstance(dataLive, dict) else []
    numAcFI = dataFI.get('total', 0) if isinstance(dataFI, dict) else 0
    dataACFI = dataFI.get('ac', []) if isinstance(dataFI, dict) else []

    df_lol = pd.DataFrame(dataACLOL)
    df_fi = pd.DataFrame(dataACFI)
    df_live = pd.DataFrame(dataACLive)

    if not df_lol.empty and 'hex' in df_lol.columns:
        df_lol = df_lol.set_index('hex')
    else:
        df_lol = pd.DataFrame(columns=['hex']).set_index('hex')

    if not df_fi.empty and 'hex' in df_fi.columns:
        df_fi = df_fi.set_index('hex')
    else:
        df_fi = pd.DataFrame(columns=['hex']).set_index('hex')

    if not df_live.empty and 'hex' in df_live.columns:
        df_live = df_live.set_index('hex')
    else:
        df_live = pd.DataFrame(columns=['hex']).set_index('hex')

    halfMergedData = df_lol.combine_first(df_fi)
    mergedData = halfMergedData.combine_first(df_live)

    numAC = max(numAcLOL, numAcFI, numAcLive)
    
    return mergedData, numAC



#-------------------------------------------------------------------
# Debugging
#-------------------------------------------------------------------

def main():
    mergedData, numAC = merger()
    mergedData.to_csv("merged_data.csv", index=True)
    print(f"Saved {len(mergedData)} rows")

if __name__ == "__main__":
    main()