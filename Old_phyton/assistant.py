# assistant.py
import os
import openai
import requests
import json

# Cargar las credenciales desde el entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("ORG")

# Variable global para almacenar el ID del hilo
thread_id = None

def assistantChat(message):
    print(type(message))
    global thread_id

    if thread_id is None:
        # Crear un nuevo hilo
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message
        )
        print(response)
        thread_id = response.get("thread", {}).get("id")
    else:
        # Continuar el hilo existente
        response = openai.ChatCompletion.create(
            model="gpt-4",
            thread=thread_id,
            messages=message
        )

    return response["choices"][0]["message"]["content"]

def get_book_titles(libro):
    url = f"https://bibliosabana.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=57US_INST&lang=es&limit=10&newspapersActive=true&newspapersSearch=false&offset=0&pcAvailability=false&q=any,contains,{libro}&qExclude=&qInclude=&rapido=false&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&searchInFulltextUserSelection=false&skipDelivery=Y&sort=rank&tab=Everything&vid=57US_INST:US"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    parsed_body = response.json()

    return [doc['pnx']['display']['title'][0] for doc in parsed_body['docs']]

def assistantWithFunctions(user_message, conversation_history):
    global thread_id

    # Definir el esquema de la función para la llamada de funciones de OpenAI
    functions = [
        {
            "name": "get_book_titles",
            "description": "Busca títulos de libros en la biblioteca de la Universidad de La Sabana",
            "parameters": {
                "type": "object",
                "properties": {
                    "libro": {
                        "type": "string",
                        "description": "El nombre del libro que quieres buscar"
                    }
                },
                "required": ["libro"]
            }
        }
    ]

    # Construir la lista de mensajes
    messages = conversation_history + [{"role": "user", "content": user_message}]

    # Llamar al asistente con funciones
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    # Verificar si se llamó a una función
    message = response["choices"][0]["message"]

    if message.get("function_call"):
        print("[Function Call]")
        function_name = message["function_call"]["name"]
        function_args = message["function_call"].get("arguments", {})

        # Verificar que function_args es un diccionario
        if isinstance(function_args, str):
            print("function_args is a string")
            function_args = json.loads(function_args)

        # Llamar a la función correspondiente
        if function_name == "get_book_titles":
            libro = function_args.get('libro', '')
            function_response = get_book_titles(libro)
        else:
            function_response = ""

        # Agregar la respuesta de la función a los mensajes
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response
        })
        # print(messages)

        # Obtener la respuesta del asistente después de la llamada a la función
        assistant_response = assistantChat(messages)
    else:
        # No se llamó a ninguna función, proceder normalmente
        assistant_response = message["content"]

    return assistant_response
