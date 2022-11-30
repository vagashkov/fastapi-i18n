from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from babel.plural import PluralRule
import glob
import json
import os
from pathlib import Path

# define project components location
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["de", "en", "ru"]
_user_language = ''


# define some middware
def add_middlewares(app):
    @app.middleware("http")
    async def get_accept_language(request: Request, call_next):
        requested_lang = request.headers.get("accept-language", None)[:2]
        global _user_language
        _user_language = DEFAULT_LANGUAGE if requested_lang not in SUPPORTED_LANGUAGES else requested_lang
        response = await call_next(request)
        return response


# create an application
app = FastAPI()
# define moddleware layers
add_middlewares(app)

# defile templates location
templates = Jinja2Templates(directory=str(BASE_DIR.joinpath('templates')))

# default language if requested is not found
default_fallback = 'en'
# languages storage
languages = {}
# rule to distinguish single from plurals
plural_rule = PluralRule({'one': 'n in 0..1'})

# load language files
languages_dir = str(BASE_DIR.joinpath('languages'))
language_list = glob.glob("{}/*.json".format(languages_dir))

for lang in language_list:
    # extract language code from filename
    filename = lang.split(os.sep)
    lang_code = filename[-1].split('.')[0]

    # and load it into languages storage
    with open(lang, 'r', encoding='utf8') as file:
        languages[lang_code] = json.load(file)


# create custom filters for Jinja2 and plural nouns
def plural_formatting(key_value, input_text, locale):
    # looking for label in selected language
    key = ''
    for i in languages[locale]:
        if key_value == languages[locale][i]:
            key = i
            break
    # label not found
    if not key:
        return key_value

    # build key name for plural value labed (bedroom -> bedroom_plural)
    plural_key = "{}_plural".format(key)

    # if plural needed and found in language file - use it
    if plural_rule(input_text) != 'one' and plural_key in languages[locale]:
        key = plural_key

    return languages[locale][key]


# assign plurals filter to Jinja2
templates.env.filters['plural_formatting'] = plural_formatting


@app.get("/apartment/", response_class=HTMLResponse)
async def rental(request: Request):
    # if language is unknown - use en
    locale = _user_language
    if locale not in languages:
        locale = default_fallback

    # bild r    esponse data
    result = {"request": request}
    # update it with translations
    result.update(languages[locale])
    # and make some data changes (to check if plurals rule is working)
    result.update({'locale': locale, 'bedroom_value': 2})

    # and finally return template-based response
    return templates.TemplateResponse("index.html", result)
