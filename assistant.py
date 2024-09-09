import openai
import os
import requests


openai.api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("ORG")


def assistantChat(user_message, conversation_history):
    conversation_history.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=conversation_history
    )
    
    chat_response = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": chat_response})
    
    return chat_response

def assistantWithFunctions(user_message, conversation_history):
    conversation_history.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=conversation_history,
        functions=[
            {
                "name": "getBookTitles",
                "description": "Get book titles from the La Universidad de La Sabana University library API. Only titles and only from La Universidad de La Sabana",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "libro": {"type": "string", 
                                  "description": "The title of the book to search for, only if it's from La Universidad de La Sabana"},
                    },
                    "required": ["libro"],
                    "additionalProperties": False,
                },
            },
        ]
    )
    
    if response['choices'][0]['finish_reason'] == 'function_call':
        function_name = response['choices'][0]['message']['function_call']['name']
        function_args = response['choices'][0]['message']['function_call']['arguments']
        
        if function_name == "getBookInfo":
            book_title = eval(function_args).get("book_title")
            book_info = get_book_titles(book_title)
            conversation_history.append({"role": "function", "name": "getBookInfo", "content": book_info})
            return book_info

    chat_response = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": chat_response})
    
    return chat_response

def get_book_titles(libro):
    url = f"https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,{libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    parsed_body = response.json()

    return [doc['pnx']['display']['title'][0] for doc in parsed_body['docs']]
