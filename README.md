# ADSB-TUI

## What is it?

Adsb-tui is a terminal user interface that gives you aircraft information of all aircraft flying with a 250 mile radius. The Program is made in python using textual and api's from adsb.lol and ipapi.co. The project was made as a execise to get rid of some rust in my programming skills. The thought behind choosing this was I needed somthing that I would use to finish the project. 

## Features

ADSB-TUI currently has Callsign, Aircraft Type, Registration, Altitude and Speed rows to display infomation. I am planning to add a radar screen with the aircrafts location in respect with the user's location. Other planned features is ssh access so you don't need to install the program, colours for aircraft that have declared an emergency, aircraft that are on the ground and military aircraft.

## Project Structure

~~~
├── displayEngine.py
├── dataCollector.py
├── ipLocation.py
└── dataFilter.py
~~~

#### `displayEngine.py`

- Entry point to the application. Houses the UI and timer for the colection of data.

#### `dataCollector.py`

- Handles the network layer, fetching raw JSON data from the API endpoints.

#### `ipLocation.py`

- Automatically geolocates your machine on the start of the application to dynamically set the coordinates of the radar. 

#### `dataFilter.py`

- Filters the data collected from the json and packages it for the UI

## How To Use

### Prereqs

Must be using Python 3.10+.

### Setup

~~~ git clone https://github.com/JackEllison4/ADSB-tui.git
cd ADSB-tui
python3 -m venv .venv
source .venv/bin/bin/activate
pip install textual requests 
~~~

### Run

``` 
source .venv/bin/activate
python3 displayEngine.py 
```

## Keybinds

| Key | Action |
| :--- | :--- |
| `q` | Exit the application safely |
| `d` | Toggle between Dark and Light mode |
| `Up` / `Down` | Scroll through the aircraft list |
| `Page Up` / `Page Down` | Jump scroll through the list |
| `Home` / `End` | Jump straight to the top or bottom of the list |

## License

This project is open-source and licensed under the GNU General Public License v3 (GPLv3). See the `LICENSE` file for more details.
