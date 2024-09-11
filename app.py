import os
from dotenv import load_dotenv
import threading
from function import gpt_call_function
from apiFunctions import get_book_titles, get_spell_info, get_wikipedia_summary


load_dotenv()

def chat_thread():
    thread_id = None
    print("ChatGPT está listo. Escribe 'exit' para salir.")
    conversation_history = []

    while True:
        user_message = input('> ')
        
        if user_message.lower() == 'exit':
            print("Saliendo del chat...")
            break

        response = gpt_call_function(user_message, thread_id)
        print(response[0])

if __name__ == "__main__":
    chat_thread = threading.Thread(target=chat_thread)
    chat_thread.start()
