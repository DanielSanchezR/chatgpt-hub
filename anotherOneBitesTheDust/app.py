import openai
import os
from dotenv import load_dotenv
import asyncio
from chat import call_chatgpt_with_functions

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
openai.api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("ORG")

# Loop de interacción con el usuario
def start_chat():
    print("ChatGPT está listo. Escribe 'exit' para salir.")

    while True:
        user_message = input('> ')

        if user_message.lower() == 'exit':
            print("Saliendo del chat...")
            break

        # Llamar a la función de ChatGPT con el mensaje del usuario
        response = asyncio.run(call_chatgpt_with_functions(user_message))
        print(response)  # Mostrar la respuesta en la consola

if __name__ == "__main__":
    start_chat()
