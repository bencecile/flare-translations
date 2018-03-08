"""
These are all of the constants that need to be cross-file
"""
from pathlib import Path

#This is the folder where all of the generated files will go
INDEX_FOLDER = Path("index")

#This is where all of the template html files live
TEMPLATES_FOLDER = Path("templates")

#This is where the top-level web assets live. JS, CSS, and anything else that will be imported by
# html
WEB_ASSETS_FOLDER = Path("webAssets")

#Update this if we add more themes
THEMES = [{
    "href": "/css/lightTheme.css",
    "id": "LightTheme",
}, {
    "href": "/css/darkTheme.css",
    "id": "DarkTheme",
}]
