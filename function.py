import openai
import os
from assistant import gpt_call_assistant
from dotenv import load_dotenv
from apiFunctions import get_book_titles, get_spell_info, get_wikipedia_summary

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Aqui se añaden las funciones que se quieren utilizar en la conversación
function = [
    {
        "name": "get_book_titles",
        "description": "Obtiene la cantidad de títulos de libros de la biblioteca de la Universidad de La Sabana através de la API de la biblioteca.",
        "parameters": {
            "type": "object",
            "properties": {
                "libro": {
                    "type": "string",
                    "description": "El titulo, filtro o palabra clave del libro que se quiere buscar."
                }
            },
            "required": ["libro"]
        }
    }
]

def gpt_call_function(user_input, thread_id):
    try:
        if thread_id is None:
            thread = None
        else:
            thread = thread_id
            
        # Create a chat completion request with function calling
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Eres AVI el asistente inteligente en español de La Universidad de la Sabana."},
                {"role": "user", "content": user_input}
            ],
            functions=function,
            function_call = 'auto'
        )

        # Extract the assistant's message
        message = response.choices[0].message.content

        # Comprobar si ChatGPT quiere llamar a la función
        if response.choices[0].message.function_call:
            function_name = response.choices[0].message.function_call.name
            function_args = response.choices[0].message.function_call.arguments
            
            if function_name == "get_book_titles":
                print("Función get_book_titles llamada")
                import json
                args = json.loads(function_args)
                book_titles = get_book_titles(args['libro'])
                book_titles2 = ', '.join(book_titles)
                natural_answer = gpt_call_assistant(book_titles2, thread)
                
                # Lista de titulos
                return natural_answer

        else:
            # Si no hay función, simplemente devuelve el mensaje de ChatGPT
            return (message, thread)
    
    except Exception as e:
        return f"Error: {str(e)}"


# Example usage:
# user_input = "Buscame el libro de El principe"
# response = gpt_call_function(user_input, None)
# print(response)