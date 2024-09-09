import requests
import os

def get_book_titles(libro):
    url = f"https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,{libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    parsed_body = response.json()

    return [doc['pnx']['display']['title'][0] for doc in parsed_body['docs']]

def get_spell_info(spell_name):
    url = f"https://www.dnd5eapi.co/api/spells/{spell_name.replace(' ', '-')}"
    response = requests.get(url)
    spell_data = response.json()

    if 'name' not in spell_data:
        print("No se ha encontrado el hechizo.")
        return
    else:
        return (f"Claro, el hechizo \"{spell_data['name']}\" es: {' '.join(spell_data['desc'])}")

def get_book_info_from_open_library(query):
    url = f"https://openlibrary.org/search.json?q={query.replace(' ', '%20')}"
    response = requests.get(url)
    data = response.json()

    books = [{'title': doc['title'], 'author_name': ', '.join(doc.get('author_name', ['Autor desconocido']))} for doc in data['docs']]

    return books

def get_anime_or_manga_info(title):
    url = f"https://api.jikan.moe/v4/search/anime?q={title.replace(' ', '%20')}"
    response = requests.get(url)
    data = response.json()

    anime_or_manga = data['data'][0]
    return {
        'title': anime_or_manga['title'],
        'tags': ', '.join([genre['name'] for genre in anime_or_manga['genres']]),
        'description': anime_or_manga['synopsis']
    }

def get_bible_passage(book, chapter, verse):
    url = f"https://api.bible/v1/bibles/06125adad2d5898a-01/verses/{book}.{chapter}.{verse}?content-type=json"
    headers = {"api-key": os.getenv("BIBLE_API_KEY")}

    response = requests.get(url, headers=headers)
    data = response.json()

    return data['data']['content']

def get_harry_potter_info(info_type):
    url = f"https://potterapi-fedeperin.vercel.app/en/{info_type}"
    response = requests.get(url)
    data = response.json()

    return data
