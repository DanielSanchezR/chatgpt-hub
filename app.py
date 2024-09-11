import os
from dotenv import load_dotenv
import threading
from assistant import assistantChat, assistantWithFunctions
from function import
from apiFunctions import get_book_titles, get_spell_info, get_wikipedia_summary


load_dotenv()

def chat_thread():
    print("ChatGPT está listo. Escribe 'exit' para salir.")
    conversation_history = []

    while True:
        user_message = input('> ')
        
        if user_message.lower() == 'exit':
            print("Saliendo del chat...")
            break

        response = assistantWithFunctions(user_message, conversation_history)
        print(response)

if __name__ == "__main__":
    chat_thread = threading.Thread(target=chat_thread)
    chat_thread.start()
