import requests
import os

# Function for getting book titles from the La Universidad de La Sabana University library API
def get_book_titles(libro):
    url = f"https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,{libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US"
    response = requests.get(url)
    
    if response.status_code == 200:
        parsed_body = response.json()
        return [doc['pnx']['display']['title'][0] for doc in parsed_body['docs']] # Return a list of book titles
    else:
        return (f"Error: Unable to fetch summary for '{topic}'")

# Function for getting spell information from the D&D API
def get_spell_info(spell_name):
    url = f"https://www.dnd5eapi.co/api/spells/{spell_name.replace(' ', '-')}"
    response = requests.get(url)

    if response.status_code == 200:
        spell_data = response.json()
        return (f"Claro, el hechizo \"{spell_data['name']}\" es: {' '.join(spell_data['desc'])}")
    else:
        return (f"Error: Unable to fetch summary for '{spell_name}'")

# Function for getting wiki summary from the Wikipedia API
def get_wikipedia_summary(topic, language="en"):
    url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract")  # Extract the summary
    else:
        return (f"Error: Unable to fetch summary for '{topic}'")
    
# Ejemplo de uso:
# valor = "El Principito"
# respuesta = get_book_titles(valor)
# print(respuesta)