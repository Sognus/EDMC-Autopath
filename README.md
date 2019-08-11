## EDMC-Autopath
EDMC-Autopath is a plugin for [Elite: Dangerous market connector](https://github.com/Marginal/EDMarketConnector). Plugin provides basic GUI to plan route using [neutron star plotter](https://www.spansh.co.uk/plotter/). If enabled by checkbox, plugin automatically update your system clipboard to next system in route. (see it in [action](https://www.youtube.com/watch?v=UDEgrHiYK24))

### Instalation
1. Make sure you have [Elite: Dangerous market connector](https://github.com/Marginal/EDMarketConnector) installed
2. Make sure EDMC version is 3.41 or newer (it might work for older versions - no guarantees)
3. Create new folder (recommended name: autopath) in EDMC plugin folder
- You can open said location by using __File -> Settings -> Plugins -> Open__ in EDMC.
- On Windows, your folder will most likely be __{DRIVE}:\Users\\{username}\AppData\Local\EDMarketConnector\plugins__ (where {username} is your - Windows' username without the brackets and {DRIVE}: is drive you system is installed on).
- If you create folder with recommended name you will put files in step 4 into __{DRIVE}:\Users\\{username}\AppData\Local\EDMarketConnector\plugins\autopath__ folder 
4. Download all files in this repository (including folder pyperclip) and copy them to created folder (default: <edmc plugin folder>/autopath/)

### Ideas & Troubleshooting
If you have any idea how to improve this plugin, create pull request with your changes or describe what would you like to have in [issues](https://github.com/Sognus/EDMC-Autopath/issues). If you find any bug, please create issue.
