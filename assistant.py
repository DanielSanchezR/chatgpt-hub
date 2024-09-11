import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_call_assistant(user_input, thread_id):

    # Crear un nuevo asistente
    assistant = client.beta.assistants.create(
        name="Assistant",
        instructions="Tu nombre es AVI y eres un asistente inteligente en español de La Universidad de la Sabana. Tu función es convertir la siguiente información, a un texto de formato plano sobre cada uno de los titulos encontrados, tienes que filtrar cada vez que te de información nueva pa crear una lista más pequeña, no repitas información.",
        model="gpt-3.5-turbo-0613",
    )
    
    # Crear o recuperar el thread
    if thread_id is None:
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(thread_id)
    
    # Crear un mensaje de asistente
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    
    # Ejecutar el thread
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Tu nombre es AVI y eres un asistente inteligente en español de La Universidad de la Sabana, tu función es convertir la siguiente información, a un texto de formato plano sobre cada uno de los titulos encontrados, tienes que filtrar cada vez que te de información nueva pa crear una lista más pequeña, no repitas información.",
    )
    
    # Comprobar el estado de la ejecución
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        
        # Si hay mensajes del asistente, obtiene el último mensaje
        if assistant_messages:
            last_message = assistant_messages[-1].content[0].text.value
        else:
            last_message = "No hay mensajes del asistente."
        
        return (last_message, thread.id)
    else:
        return (thread.id, "El estado de la ejecución no fue completado.")

# Ejemplo de uso
# thread_id, last_message = gpt_call_assistant("¿De qué color es el sol?", None)
# print(f"Thread ID: {thread_id}")
# print(f"Último mensaje del asistente: {last_message}")
