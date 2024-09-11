import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_call_assistant(user_input, thread_id=None):
    print("Iniciando conversación con ChatGPT...")

    # Crear un nuevo asistente
    assistant = client.beta.assistants.create(
        name="Assistant",
        instructions="Tu nombre es AVI y eres un asistente inteligente en español de La Universidad de la Sabana.",
        model="gpt-3.5-turbo-0613",
    )
    
    # Crear o recuperar el thread
    if thread_id is None:
        thread = client.beta.threads.create()
        print(f"Nuevo thread creado con ID: {thread.id}")
    else:
        thread = client.beta.threads.retrieve(thread_id)
        print(f"Usando thread existente con ID: {thread.id}")
    
    # Crear un mensaje de asistente
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Tu nombre es AVI y eres un asistente inteligente en español de La Universidad de la Sabana."
    )
    
    if run.status == 'completed': 
        # Obtener y mostrar los mensajes
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages.data:
            role = message.role
            content = message.content[0].text.value  # Acceder al texto del mensaje
            print(f"{role}: {content}")
        return thread.id  # Retorna el ID del thread para seguir la conversación
    else:
        print(run.status)

# Primer llamado - No usa thread
thread_id = gpt_call_assistant("¿De qué color es el sol?", None)

# Segundo llamado - Usa el thread creado
gpt_call_assistant("¿Qué fue lo que me dijiste?", thread_id)
