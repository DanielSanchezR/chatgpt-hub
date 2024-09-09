import openai
import json
import asyncio
from api_request import (
    get_book_titles,
    get_spell_info,
    get_book_info_from_open_library,
    get_anime_or_manga_info,
    get_bible_passage,
    get_harry_potter_info
)

async def call_chatgpt_with_functions(user_message):
    chat = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Perform function request for the user"},
            {"role": "user", "content": user_message},
        ],
        functions=[
            {
                "name": "getBookTitles",
                "description": "Get book titles from the La Universidad de La Sabana University library API. Only titles and only from La Universidad de La Sabana",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "libro": {"type": "string", "description": "The title of the book to search for, only if it's from La Universidad de La Sabana"},
                    },
                    "required": ["libro"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "getSpellInfo",
                "description": "Get information about a spell from the D&D API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spellName": {"type": "string", "description": "The spell name must be in English, if it needs translation do it. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')"},
                    },
                    "required": ["spellName"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "getBookInfoFromOpenLibrary",
                "description": "Get book information (titles and authors) from Open Library API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query for titles or authors"},
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "getAnimeOrMangaInfo",
                "description": "Get information about an anime or manga from MyAnimeList. Provides title, tags, and description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The name of the anime or manga to search for. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')"},
                    },
                    "required": ["title"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "getBiblePassage",
                "description": "Get specific passages from the Bible. Requires the book, chapter, and verse.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book": {"type": "string", "description": "The book of the Bible. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')"},
                        "chapter": {"type": "integer", "description": "The chapter in the book. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')"},
                        "verse": {"type": "integer", "description": "The specific verse in the chapter. If it consists of two or more words, remove the spaces and connect them with a hyphen ('-')"},
                    },
                    "required": ["book", "chapter", "verse"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "getHarryPotterInfo",
                "description": "Get information about Harry Potter, including books, characters, houses, and spells.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["books", "characters", "houses", "spells"],
                            "description": "The type of information to retrieve from Harry Potter: books, characters, houses, or spells.",
                        }
                    },
                    "required": ["type"],
                    "additionalProperties": False,
                },
            }
        ],
        function_call="auto",
    )

    wants_to_use_function = chat['choices'][0]['finish_reason'] == "function_call"

    if wants_to_use_function:
        function_name = chat['choices'][0]['message']['function_call']['name']
        argument_obj = json.loads(chat['choices'][0]['message']['function_call']['arguments'])

        # Ejecutar la función correspondiente
        response = await handle_function_call(function_name, argument_obj)
        return response
    else:
        # Si no se necesita una función, se devuelve la respuesta directamente en lenguaje natural
        return chat['choices'][0]['message']['content']

async def handle_function_call(function_name, arguments):
    if function_name == "getBookTitles":
        titles = get_book_titles(arguments['libro'])
        return await natural_language_response(titles)
    elif function_name == "getSpellInfo":
        spell_info = get_spell_info(arguments['spellName'])
        return await natural_language_response(spell_info)
    elif function_name == "getBookInfoFromOpenLibrary":
        books = get_book_info_from_open_library(arguments['query'])
        return await natural_language_response(books)
    elif function_name == "getAnimeOrMangaInfo":
        anime_info = get_anime_or_manga_info(arguments['title'])
        return await natural_language_response(anime_info)
    elif function_name == "getBiblePassage":
        passage = get_bible_passage(arguments['book'], arguments['chapter'], arguments['verse'])
        return await natural_language_response(passage)
    elif function_name == "getHarryPotterInfo":
        harry_potter_info = get_harry_potter_info(arguments['type'])
        return await natural_language_response(harry_potter_info)

async def natural_language_response(data):
    # Convierte los datos en un string comprensible para enviarlo a ChatGPT
    data_str = json.dumps(data, indent=2)
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Convierte estos datos en una respuesta en lenguaje natural"},
            {"role": "user", "content": f"Datos obtenidos: {data_str}"},
        ]
    )

    return response['choices'][0]['message']['content']
