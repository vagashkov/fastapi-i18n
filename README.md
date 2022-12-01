# fastapi-i18n
Simple JSON-based internationalization sample


To view demo:
- clone this repo
- navigate to fastapi-i18n directory
- create fresh venv and activate it
- install packages according to requirements.txt file
- launch application with 'uvicorn src.apart_app:app' command
- use cURL command curl -H 'Accept-Language:en-EN' 127.0.0.1:8000/apartment/ to get page in English
- than use cURL command curl -H 'Accept-Language:de-DE' 127.0.0.1:8000/apartment/ to ger page in German
- also cURL command curl -H 'Accept-Language:ru-RU' 127.0.0.1:8000/apartment/ to view page in Russian
- finally use cURL command curl -H 'Accept-Language:fr-FR' 127.0.0.1:8000/apartment/ to view page in English cause we don't speak French
