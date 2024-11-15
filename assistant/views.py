from django.shortcuts import render, redirect
#from .models import Thread, Message, Visitor 
from django.http import JsonResponse
import json
import time
from IPython.display import display
import os 
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from openai import OpenAI

API_KEY=os.getenv('OPENAI_API_KEY')
ASSISTANT_ID= "asst_6tSMEXtaC23I2diV8Z5jdXWX"

client = OpenAI(api_key=API_KEY)

#assistan

def show_json(obj):
    display(json.loads(obj.model_dump_json()))
'''
my_assistant = client.beta.assistants.retrieve("asst_6tSMEXtaC23I2diV8Z5jdXWX")
show_json(my_assistant)

'''




#Create a thread 
#Add message to thread 
#Run the thread 

#add message
#Run the thread 
#retrive the message of the thread 
#



#thread
thread = client.beta.threads.create()


#Add message to thread 
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="quisiera un pollo ranchero"
)

#Run the thread 

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id="asst_6tSMEXtaC23I2diV8Z5jdXWX"
 # stream=True,
)
    

message_retrieve = client.beta.threads.messages.retrieve(
  message_id=message.id,
  thread_id=thread.id,
)
print(message_retrieve)




'''def visitor_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Verificar si el visitante ya existe
        visitor, created = Visitor.objects.get_or_create(email=email, defaults={'name': name})

        # Guardar el visitor_id en la sesión
        request.session['visitor_id'] = visitor.id

        return redirect('chat')

    return render(request, 'chat/visitor_info.html')

'''
'''
def visitor_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Crear un nuevo visitante sin importar si ya existe uno con el mismo correo
        visitor = Visitor.objects.create(name=name, email=email)

        # Guardar el visitor_id en la sesión
        request.session['visitor_id'] = visitor.id

        return redirect('chat')

    return render(request, 'chat/visitor_info.html')




def chat(request):
   

    # Verificar si el visitor_id está en la sesión
    if 'visitor_id' not in request.session:
        return redirect('visitor_info')

    visitor = Visitor.objects.get(id=request.session['visitor_id'])

    # Verificar si el thread_id está en la sesión
    if 'thread_id' in request.session:
        # Crear un nuevo hilo utilizando la API de OpenAI
        openai_thread = client.beta.threads.create()
        thread_id = openai_thread.id 
        # Guardar el hilo en la base de datos
        thread = Thread.objects.create(visitor=visitor, thread_id=thread_id)
        # Guardar el thread_id en la sesión
        request.session['thread_id'] = thread_id
    else:
        thread_id = request.session['thread_id']
        # Obtener el hilo de la base de datos
        thread = Thread.objects.get(thread_id=thread_id)

    if request.method == 'POST':
        user_message_content = request.POST.get('message')

        # Enviar el mensaje del usuario al hilo de OpenAI
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message_content
        )

        # Guardar el mensaje del usuario en la base de datos
        Message.objects.create(thread=thread, role='user', content=user_message_content)

        # Ejecutar el hilo
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,  # Asegúrate de usar el assistant_id correcto
            stream=True,
        )
        
        # Obtener la respuesta del asistente
        thread_messages = client.beta.threads.messages.list(thread_id, order="asc" )
        thread_messages_list = list(thread_messages)
        # Procesar los mensajes
        
        for m in thread_messages_list:
            role = m.role
            content = m.content[0].text.value
            # Verifica si el mensaje ya está en la base de datos para evitar duplicados
            if not Message.objects.filter(thread=thread, role=role, content=content).exists():
               Message.objects.create(thread=thread, role=role, content=content)
        
        
        
        #Message.objects.create(thread=thread, role=m.role, content=assistant_reply_content)
            

        # Obtener todos los mensajes para mostrar
        messages = Message.objects.filter(thread=thread).order_by('created_at')

        return render(request, 'chat/chat.html', {'messages': messages, 'visitor': visitor})

    else:
        # En caso de GET, mostrar los mensajes existentes
        messages = Message.objects.filter(thread=thread).order_by('created_at')
        return render(request, 'chat/chat.html', {'messages': messages, 'visitor': visitor})'''


