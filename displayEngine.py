# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.driver import Driver
from textual.widgets import Footer, Header, DataTable

from dataFilter import adsb_filter
from radarCanvas import RadarCanvas

class adsbApp(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [("q", "quit", "Exit the App"),
                ("up", "cursor_up", "Cursor up"),
                ("down", "cursor_down", "Cursor down"),
                ("right", "cursor_right", "Cursor right"),
                ("left", "cursor_left", "Cursor left"),
            ]    

    def compose(self) -> ComposeResult:
        yield Header()
        with Grid(id="app-layout"):
            yield DataTable(id="telemetry-table")
            yield RadarCanvas(id="radar-screen")
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Callsign","Aircraft Type", "Registration", "Altitude (ft)", "Speed (kts)", "Year", "Owner")
        await self.refresh_radar()
        self.set_interval(30, self.refresh_radar)
    
    async def refresh_radar(self) -> None:       
        (numAc, AcType, AcReg, callsign, alt, speed, lat, lon, emergency, military, year, owner) = adsb_filter()
        table = self.query_one(DataTable)
        table.clear()
        for i in range(len(callsign)):
            if emergency[i] not in ("none", None):
                table.add_row(
                    f"[red]{callsign[i]}[/red]", 
                    f"[red]{AcType[i]}[/red]", 
                    f"[red]{AcReg[i]}[/red]", 
                    f"[red]{str(alt[i])}[/red]", 
                    f"[red]{str(speed[i])}[/red]",
                    f"[red]{str(year[i])}[/red]",
                    f"[red]{str(owner[i])}[/red]",
                )

            elif military[i]:
                table.add_row(
                    f"[green]{callsign[i]}[/green]", 
                    f"[green]{AcType[i]}[/green]", 
                    f"[green]{AcReg[i]}[/green]", 
                    f"[green]{str(alt[i])}[/green]", 
                    f"[green]{str(speed[i])}[/green]",
                    f"[green]{str(year[i])}[/green]",
                    f"[green]{str(owner[i])}[/green]",
                )

            else:
                table.add_row(callsign[i], AcType[i], AcReg[i], str(alt[i]), str(speed[i]), str(year[i]), str(owner[i]))  
                
        radar = self.query_one(RadarCanvas)
        radar.update_data(lon, lat, callsign, military, emergency)

if __name__ == "__main__":
    app = adsbApp()
    app.run()