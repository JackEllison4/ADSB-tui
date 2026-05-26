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
    
    numAcLOL = dataLOL['total']
    dataACLOL = dataLOL['ac']
    numAcLive = dataLive['total']
    dataACLive = dataLive['ac']
    numAcFI = dataFI['total']
    dataACFI = dataFI['ac']

    df_lol = pd.DataFrame(dataACLOL)
    df_fi = pd.DataFrame(dataACFI)
    df_live = pd.DataFrame(dataACLive)


    df_lol = df_lol.set_index('hex')
    df_fi = df_fi.set_index('hex')
    df_live = df_live.set_index('hex')

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