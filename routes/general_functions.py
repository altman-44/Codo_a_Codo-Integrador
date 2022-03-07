import os
from flask import render_template
import time
def render_layout_template(tmpl_name, **kwargs):
    fontawesomeKitJsUrl = os.getenv('FONTAWESOME_KIT_JS_URL')
    return render_template(tmpl_name, fontawesomeKitJsUrl=fontawesomeKitJsUrl, **kwargs)

def getParamsFromUrl(url):
    result = {}
    invertedUrl = url[::-1]
    path = invertedUrl[0:invertedUrl.find('/')][::-1]
    questionMarkIndex = path.find('?')
    if questionMarkIndex > -1:
        pathDivided = path[questionMarkIndex + 1:len(path)].split('&')
        for paramPart in pathDivided:
            splittedParam = paramPart.split('=')
            result[splittedParam[0]] = splittedParam[1]
    return result