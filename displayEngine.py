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
from dataCollector import colector

class adsbApp(App):

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit", "Exit the App"),
                ("enter", "select_cursor", "Select"),
                ("up", "cursor_up", "Cursor up"),
                ("down", "cursor_down", "Cursor down"),
                ("right", "cursor_right", "Cursor right"),
                ("left", "cursor_left", "Cursor left"),
                ("pageup", "page_up", "Page up"),
                ("pagedown", "page_down", "Page down"),
                ("ctrl+home", "scroll_top", "Top"),
                ("ctrl+end", "scroll_bottom", "Bottom"),
                ("home", "scroll_home", "Home"),
                ("end", "scroll_end", "End")
                
            ]    

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Callsign","Aircraft Type", "Registration", "Altitude (ft)", "Speed (kts)")
        await self.refresh_radar()
        self.set_interval(60, self.refresh_radar)
    
    async def refresh_radar(self) -> None:
        dataIn = colector()
        numAc, AcType, AcReg, callsign, alt, speed = adsb_filter(dataIn)
        table = self.query_one(DataTable)
        for i in range(numAc):
            table.add_row(callsign[i], AcType[i], AcReg[i], str(alt[i]), str(speed[i]))
        

if __name__ == "__main__":
    app = adsbApp()
    app.run()