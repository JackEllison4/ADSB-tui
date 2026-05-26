# Copyright (C) 2026 Jack Ellison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import math
from textual.widget import Widget
from rich.text import Text

import dataCollector

class RadarCanvas(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aircraft_data = []
        self.lon = dataCollector.lon
        self.lat = dataCollector.lat
    
    def update_data(self, lon_list, lat_list, callsign_list, mil_list, em_list):
        self.aircraft_data = list(zip(lon_list, lat_list, callsign_list, mil_list, em_list))
        self.refresh()

    def render(self):
        width = self.size.width
        height = self.size.height

        if width < 3 or height < 3:
            return Text("")

        grid = [[" " for _ in range(width)] for _ in range(height)]

        center_x = width // 2
        center_y = height // 2

        grid[center_y][center_x] = "+" 

        aspect_multiplier = 2.8

        max_radius = min(center_x / aspect_multiplier, center_y) - 2
        
        if max_radius < 2:
            max_radius = 2

        for radius_scale in [0.33, 0.66, 1.0]:
            current_r = max_radius * radius_scale
            num_steps = int(4.0 * math.pi * current_r * aspect_multiplier)
            
            if num_steps < 16:
                num_steps = 16

            for step in range(num_steps):
                rad = (step / num_steps) * 2.0 * math.pi
                x = round(center_x + (current_r * math.sin(rad) * aspect_multiplier))
                y = round(center_y - (current_r * math.cos(rad)))
                
                if 0 <= x < width and 0 <= y < height:
                    if x == center_x and y == center_y:
                        continue
                    
                    vx = x - center_x
                    vy = (y - center_y) * aspect_multiplier
                    
                    if vy == 0:
                        char = "│"
                    
                    else:
                        slope = abs(vx / vy)
                        
                        if slope < 0.28:
                            char = "─"
                        
                        elif slope > 3.5:
                            char = "│"
                        
                        else:
                            if (vx * (y - center_y)) < 0:
                                char = "╲"
                            
                            else:
                                char = "╱"
                        
                    grid[y][x] = f"[dim green]{char}[/dim green]"

        deg_range = 4

        occupied = [[False for _ in range(width)] for _ in range(height)]

        for lon, lat, call, mil, em in self.aircraft_data:
            if lat == 0.0 or lon == 0.0:
                continue

            relative_lat = lat - self.lat
            relative_lon = lon - self.lon

            norm_lon = relative_lon / deg_range
            norm_lat = relative_lat / deg_range

            if norm_lon**2 + norm_lat**2 > 0.95:
                continue

            x_offset = round(norm_lon * max_radius * aspect_multiplier)
            y_offset = round(norm_lat * max_radius)
            
            plane_x = center_x + x_offset
            plane_y = center_y - y_offset

            if 0 <= plane_x < width and 0 <= plane_y < height:
                if em not in ("none", None):
                    tag = "red"
                    symbol = "*"
                
                elif mil:
                    tag = "green"
                    symbol = "*"
                
                else:
                    tag = "white"
                    symbol = "*"

                grid[plane_y][plane_x] = f"[{tag}]{symbol}[/{tag}]"
                occupied[plane_y][plane_x] = True

                label = call[:3].strip() if call != 'N/A' else '???'

                offsets = [
                    (1, 0),    
                    (-4, 0),   
                    (-1, 1),   
                    (-1, -1)  
                ]

                for dx, dy in offsets:
                    lx = plane_x + dx
                    ly = plane_y + dy

                    if 0 <= ly < height and 0 <= lx < width and lx + len(label) <= width:
                        if not any(occupied[ly][lx + k] for k in range(len(label))):
                            for k, char in enumerate(label):
                                grid[ly][lx + k] = f"[{tag}]{char}[/{tag}]"
                                occupied[ly][lx + k] = True
                            break

        output_lines = ["".join(row) for row in grid]
        return Text.from_markup("\n".join(output_lines))