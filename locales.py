from pathlib import Path


from constants import INDEX_FOLDER, THEMES
from template import templateHTML

class Locales:
    """
    Makes it easy to keep track of all the different locales that we can have
    """
    def __init__(self, templateParams, localeStrings):
        """
        Gives templateParams which can later be referenced with the paramKeyList on some methods.
        localeStrings are given every single templated HTML file.
        """
        self.languages = ["JP", "EN"]
        self.localNames = {
            "JP": "日本語",
            "EN": "English",
        }
        self.folders = {
            "JP": INDEX_FOLDER / "jp",
            "EN": INDEX_FOLDER / "en",
        }
        # Fixes the parameters by creating a normalized dictionary for each language.
        # Keeps these parameters for the template HTML command
        self.templateParams = {
            lang: self.fixParams(lang, templateParams) for lang in self.languages
        }
        self.localeStrings = {
            lang: self.fixParams(lang, localeStrings) for lang in self.languages
        }

    ######################Public Methods######################

    def templateHTML(self, children, templateName, paramKeyList):
        """
        Templates HTML with a few differences:

        It will place a templated HTML file at the bottom of children for every language.

        It will use the paramKeyList to access the correct dictionary when templating.
        """
        folders = self.getNestedLanguageFolders(children)
        for lang in self.languages:
            params = nestedElement(self.templateParams[lang], paramKeyList)
            #Also put the locale strings at the top level of the template parameters
            params["strings"] = self.localeStrings[lang]
            params["themes"] = THEMES
            templateHTML(templateName, folders[lang], params)

    def makeFolders(self, children = []):
        """
        Creates folders for the different languages.
        """
        folders = self.getNestedLanguageFolders(children)
        for lang in self.languages:
            folders[lang].mkdir(exist_ok=True)

    ######################Private Methods######################

    def getNestedLanguageFolders(self, children = []):
        """
        Returns a list of paths where the children are nested correctly for each language

        If any children are specified, then the previous element is the next element's parent.
        Each element should only be a single part of a path and always relative.
        They are created underneath every language.
        """
        childPath = nestedPath(children)
        return { lang: self.folders[lang] / childPath for lang in self.languages }

    def doesKeyMatch(self, key, matchLang):
        """
        Returns True if the key has the same language suffix as matchLang at the end of the
        key or if there isn't a language suffix at all. Only returns false if the key has a  
        language suffix that isn't matchLang.
        """
        for lang in self.languages:
            if isinstance(key, str) and key.endswith(lang) and lang != matchLang:
                return False

        return True

    def fixParams(self, lang, templateParams):
        """
        Not meant to be used from the outside.

        Fixes the template parameters for the given language, recursively on the params.

        In the templateParams, if a key ends with a language identifier (eg. JP or EN), then it will
        be used without the suffix for the correct language. (eg. { "titleJP": "titleInJp",
        "titleEN": "titleInEn" } => { "title": "titleInJp" } for Japanese and
        { "title": "titleInEn" } for English).
        """
        if isinstance(templateParams, list):
            #Just fix all of the params for every element in the list
            realParams = [self.fixParams(lang, item) for item in templateParams]
        #It is a dictionary here, always
        else:
            #Set the language at every level of the params so that no matter what level is being
            # templated, it will always be given to the templater
            realParams = {
                "lang": lang,
                "localNames": self.localNames,
            }
            for key in templateParams:
                if not self.doesKeyMatch(key, lang):
                    continue

                #We need to do special parsing for the content key because it will have mixed
                # english and japanese
                if key == "content":
                    realContent = []

                    grabNextLine = True
                    for line in templateParams[key].strip().splitlines():
                        if line == (">%s" % lang):
                            #Grab the next line if the language marker matches
                            grabNextLine = True
                            continue
                        elif line.startswith(">"):
                            #Ignore the next line after a language marker that isn't lang
                            grabNextLine = False
                            continue

                        #Grab the line if it's an empty string. This will be used for formatting
                        #Also grab the line if we need to
                        if line == "" or grabNextLine:
                            realContent.append(line)
                            
                    realParams["content"] = realContent                    
                elif isinstance(templateParams[key], (list, dict)):
                    #Fix all of the params for the list or dictionary
                    #We can do a replace just in case we need diverging trees based on language
                    realParams[key.replace(lang, "")] = self.fixParams(lang, templateParams[key])
                else:
                    realParams[key.replace(lang, "")] = templateParams[key]

        return realParams

def nestedPath(children):
    """
    Creates a nested path from a list of children
    """
    temp = Path()
    for child in children:
        temp /= child

    return temp

def nestedElement(keyable, keyList):
    element = keyable
    for key in keyList:
        element = element[key]

    return element
