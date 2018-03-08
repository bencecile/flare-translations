import re

from jinja2 import Environment, FileSystemLoader


from constants import INDEX_FOLDER, TEMPLATES_FOLDER, WEB_ASSETS_FOLDER

templateEnvironment = Environment(
    loader=FileSystemLoader( str(TEMPLATES_FOLDER.resolve()) ),
    autoescape=True,
    auto_reload=False,
)

assetEnvironment = Environment(
    loader=FileSystemLoader( str(WEB_ASSETS_FOLDER.resolve()) ),
    variable_start_string="$<",
    variable_end_string=">$",
)

#Templating Regexes
SPACE_REPLACE = re.compile(r" {2,}")
NEWLINE_REPLACE = re.compile(r"[\r\n]")
HTML_COMMENT_REPLACE = re.compile(r"<!--(?:.(?!-->))*.-->", re.S)

JS_1_LINE_COMMENT_REPLACE = re.compile(r"\/\/.*")
MUTLI_LINE_COMMENT_REPLACE = re.compile(r"\/\*(.(?!\*\/))*.\*\/", re.S)

def templateHTML(templateName, baseFolder, templateParams):
    """
    Templates an HTML file.
    The template name should just be the name with no either path specifiers (eg. "index" will give
    you the file templates/index.html).

    Writes the templated HTML into an index.html inside of the baseFolder.
    """
    #This will throw if the template cannot be found
    template = templateEnvironment.get_template("%s.html" % templateName)
    templatedHTML = template.render(templateParams)

    templatedHTML = re.sub(NEWLINE_REPLACE, "", templatedHTML)
    templatedHTML = re.sub(SPACE_REPLACE, "", templatedHTML)
    templatedHTML = re.sub(HTML_COMMENT_REPLACE, "", templatedHTML)

    (baseFolder / "index.html").write_text(templatedHTML, encoding="UTF-8")

def templateAsset(templateName, fileType, templateParams):
    """
    Templates a web asset that matches the given name and type.
    """
    path = "%s/%s.%s" % (fileType, templateName, fileType)
    template = assetEnvironment.get_template(path)
    templatedText = template.render(templateParams)
    
    if fileType == "js":
        templatedText = re.sub(JS_1_LINE_COMMENT_REPLACE, "", templatedText)
    templatedText = re.sub(MUTLI_LINE_COMMENT_REPLACE, "", templatedText)
    templatedText = re.sub(NEWLINE_REPLACE, "", templatedText)
    templatedText = re.sub(SPACE_REPLACE, "", templatedText)
    
    (INDEX_FOLDER / path).write_text(templatedText, encoding="UTF-8")
