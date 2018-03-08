from pathlib import Path
import re
from datetime import datetime


from constants import INDEX_FOLDER, THEMES, WEB_ASSETS_FOLDER
from locales import Locales
import localeStrings
from template import templateAsset, templateHTML
import ReZero

#Keep a list of all the possible novels that we have
#We need the top most level to be a dictionary for templating
NOVELS = {
    "novels": [
        ReZero.description,
    ]
}

JS_PARAMS = {
    "themes": THEMES,
    "themeStorageKey": "theme",
}

CSS_PARAMS = {
    "mainLight": "#f0f0f0",
    "mainDark": "#303030",

    "headerLight": "#ffae00",
    "headerDark": "#7700ff",

    "accentLight": "#d0d0d0",
    "accentDark": "#505050",
}

def build():
    INDEX_FOLDER.mkdir(exist_ok=True)
    #Just do a redirect to the English site at the very top level
    templateHTML("redirect", INDEX_FOLDER, { "redirectLocation": "/en" })

    #Move any of our web assets into the index folder
    for path in WEB_ASSETS_FOLDER.rglob("*.*"):
        #This is the destination file underneath the index
        destFile = INDEX_FOLDER / path.relative_to(WEB_ASSETS_FOLDER)
        destFile.parent.mkdir(exist_ok=True, parents=True)

        #Minify any JS or CSS files instead writing it raw
        if destFile.suffix == ".js":
            templateAsset(path.stem, "js", JS_PARAMS)
        elif destFile.suffix == ".css":
            templateAsset(path.stem, "css", CSS_PARAMS)
        else:
            destFile.write_bytes(path.read_bytes())

    #Create the locales object that we will be using for everything
    locales = Locales(NOVELS, localeStrings.strings)

    #Create the topmost level language folders
    locales.makeFolders()

    #Move a top level index.html into each language folder. This will be for novel navigation, a
    # short version of the synopsis, the author and a good cover image
    locales.templateHTML([], "top", [])
    
    keyList = ["novels"]
    for (novelNum, novel) in enumerate(NOVELS["novels"]):
        keyList.append(novelNum)
        folderLevel = [ novel["urlName"] ]
        locales.makeFolders(folderLevel)

    
    print("Finished building at", datetime.now().isoformat())

if __name__ == "__main__":
    build()
