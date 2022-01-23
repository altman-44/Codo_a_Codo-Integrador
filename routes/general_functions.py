import os
from flask import render_template

def render_layout_template(tmpl_name, **kwargs):
    fontawesomeKitJsUrl = os.getenv('FONTAWESOME_KIT_JS_URL')
    return render_template(tmpl_name, fontawesomeKitJsUrl=fontawesomeKitJsUrl, **kwargs)