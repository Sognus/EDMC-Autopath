# EDMC-Autopath
EDMC-Autopath is a plugin for [Elite: Dangerous Market Connector](https://github.com/Marginal/EDMarketConnector). This plugin provides a basic GUI to plan routes using the [neutron star plotter](https://www.spansh.co.uk/plotter/). If enabled the plugin will automatically update your system clipboard to the next system in route. [See it in action](https://www.youtube.com/watch?v=UDEgrHiYK24).

## Installation
1. Install [Elite: Dangerous Market Connector](https://github.com/Marginal/EDMarketConnector)(tested on 3.41+, might work on older versions but no guarantees).
2. Create new folder (recommended name: `autopath`) in EDMC plugin folder.
- You can open said location by using __File -> Settings -> Plugins -> Open__ in EDMC.
- On Windows, your folder will most likely be __{DRIVE}:\Users\\{username}\AppData\Local\EDMarketConnector\plugins__ (where {username} is your - Windows' username without the brackets and {DRIVE}: is drive you system is installed on).
- If you create folder with recommended name you will put files in step 3 into __{DRIVE}:\Users\\{username}\AppData\Local\EDMarketConnector\plugins\autopath__ folder 
3. Download all files in this repository (including the `pyperclip` folder) and copy them to the created folder (default: <edmc plugin folder>/autopath/).

## Ideas & Troubleshooting
If you have any ideas on how to improve this plugin, create a pull request with your changes or describe what you would like in an [issue](https://github.com/Sognus/EDMC-Autopath/issues). If you find any bugs, please [create an issue](https://github.com/Sognus/EDMC-Autopath/issues).
